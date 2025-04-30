# core/admin.py
from .models import Product, Order, Review
from reportlab.lib.pagesizes import A4
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from .models import Report
from .utils import generate_sales_report
import matplotlib.pyplot as plt
import io
import base64
import csv
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.conf import settings
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'rating', 'is_popular', 'created_by')
    list_filter = ('category', 'is_popular', 'rating')
    search_fields = ('name',)
    verbose_name = _('Продукт')
    verbose_name_plural = _('Продукты')

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_products', 'get_user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('items__product')

    def get_products(self, obj):
        links = [
            f'<a href="/admin/core/product/{item.product.id}/change/">{item.product.name}</a>'
            for item in obj.items.all()
        ]
        return mark_safe("<br>".join(links))

    get_products.short_description = _('Товары')
    get_products.allow_tags = True

    def get_user(self, obj):
        return obj.user.username if obj.user else "Анонимный пользователь"
    get_user.short_description = _('Пользователь')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name',)
    verbose_name = _('Отзыв')
    verbose_name_plural = _('Отзывы')

# Объединяем функциональность SalesReportAdmin и ReportAdmin
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/sales_report.html"
    list_display = ('created_at', 'total_sales', 'total_orders', 'total_customers')
    ordering = ('-created_at',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales_report/', self.admin_site.admin_view(self.sales_report_view), name='sales_report'),
            path('download_csv/', self.admin_site.admin_view(self.download_sales_report_csv), name='download_sales_report_csv'),
            path('download_pdf/', self.admin_site.admin_view(self.download_sales_report_pdf), name='download_sales_report_pdf'),
        ]
        return custom_urls + urls

    def sales_report_view(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        print(f"Received start_date: {start_date}, end_date: {end_date}")  # Отладка

        # Генерируем отчёт по продажам
        report = generate_sales_report(start_date, end_date)

        print(f"Generated report: {report}")  # Отладка

        # Проверяем наличие ключа 'sales_data'
        if 'sales_data' not in report:
            print("Error: 'sales_data' not in report")
            # Здесь можно добавить обработку ошибки или избежать перенаправления

        # Генерируем график продаж
        graph_html = self.get_sales_graph(report.get('sales_data', []))

        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'report': report,
            'start_date': start_date,
            'end_date': end_date,
            'graph_html': graph_html,
        }
        return render(request, 'admin/sales_report.html', context)

    def get_sales_graph(self, sales_data):
        if not sales_data:
            return "<p>Нет данных для отображения графика.</p>"

        # Пример генерации графика с использованием matplotlib
        dates = [data['date_only'].strftime('%Y-%m-%d') for data in sales_data]
        totals = [float(data['total']) for data in sales_data]  # Убедитесь, что это числа

        plt.figure(figsize=(10, 5))
        plt.plot(dates, totals, marker='o', linestyle='-', color='b')
        plt.title('Продажи по дням')
        plt.xlabel('Дата')
        plt.ylabel('Общая сумма продаж')
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graph = base64.b64encode(image_png).decode('utf-8')
        plt.close()

        return mark_safe(f'<img src="data:image/png;base64,{graph}"/>')

    def download_sales_report_csv(self, request):
        import codecs

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        report = generate_sales_report(start_date, end_date)

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

        # Добавляем BOM для корректного отображения в Excel
        response.write(codecs.BOM_UTF8)

        writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        # Записываем заголовки с кодировкой
        writer.writerow(['Дата', 'Общий объем продаж', 'Общее количество заказов', 'Общее количество клиентов'])

        writer.writerow([timezone.now().strftime('%Y-%m-%d'), report['total_sales'], report['total_orders'],
                         report['total_customers']])

        # Проверяем наличие данных о продажах
        if 'sales_data' in report and report['sales_data']:
            writer.writerow([])
            writer.writerow(['Дата', 'Сумма продаж'])
            for data in report['sales_data']:
                writer.writerow([data['date_only'].strftime('%Y-%m-%d'), data['total']])
        else:
            writer.writerow([])
            writer.writerow(['Нет данных о продажах за выбранный период.'])

        return response

    def download_sales_report_pdf(self, request):
        # Регистрация шрифта, поддерживающего кириллицу
        font_path = os.path.join(settings.BASE_DIR, 'core', 'fonts', 'DejaVuSans.ttf')
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        report = generate_sales_report(start_date, end_date)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        p.setFont('DejaVuSans', 12)

        p.drawString(100, 800, "Отчет по продажам")

        # Выводим общие показатели
        p.drawString(100, 780, f"Общий объем продаж: {report['total_sales']}")
        p.drawString(100, 760, f"Общее количество заказов: {report['total_orders']}")
        p.drawString(100, 740, f"Общее количество клиентов: {report['total_customers']}")

        # Проверяем наличие данных о продажах
        y = 700
        if 'sales_data' in report and report['sales_data']:
            p.drawString(100, y, "Продажи по дням:")
            y -= 20
            for data in report['sales_data']:
                p.drawString(100, y, f"{data['date_only'].strftime('%Y-%m-%d')}: {data['total']}")
                y -= 20
                if y < 50:
                    p.showPage()
                    p.setFont('DejaVuSans', 12)
                    y = 800
        else:
            p.drawString(100, y, "Нет данных о продажах за выбранный период.")

        p.showPage()
        p.save()

        return response

    def changelist_view(self, request, extra_context=None):
        report = generate_sales_report()
        extra_context = extra_context or {}
        extra_context['report'] = report
        return super().changelist_view(request, extra_context=extra_context)
