import pandas as pd
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generar_pdf(df, ventas, pdf_salida):
    doc = SimpleDocTemplate(pdf_salida, pagesize=A4)
    elementos = []
    estilo = getSampleStyleSheet()

    titulo = Paragraph(f"Reporte de Ventas - {datetime.today().strftime('%d-%m-%Y')}", estilo['Heading1'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 12))

    headers = df.columns.tolist()
    data_list = [headers] + df.values.tolist()

    tabla = Table(data_list)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 20))

    summary = Paragraph(f"<b>Facturacion total:</b> {ventas:,.2f}€", estilo['Normal'])
    elementos.append(summary)

    doc.build(elementos)


def main():
    entrada_csv = 'sales.csv'
    salida_pdf = 'reporte_mensual.pdf'

    try:
        df = pd.read_csv(entrada_csv)

        df['subtotal'] = df['cantidad'] * df['precio_unitario']
        facturacion = df['subtotal'].sum()

        df['precio_unitario'] = df['precio_unitario'].apply(lambda x: f"{x:,.2f}€")
        df['subtotal'] = df['subtotal'].apply(lambda x: f"{x:,.2f}€")


        generar_pdf(df, facturacion, salida_pdf)
        print(f"[OK] Reporte generado: {salida_pdf} | Total procesado: {facturacion:,.2f}€")

    except FileNotFoundError:
        print(f"[ERROR] No se encontro el archivo {entrada_csv}.")
    except Exception as e:
        print(f"[ERROR] Fallo en la generacion del reporte: {e}")


if __name__ == "__main__":
    main()