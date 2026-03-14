import smtplib
import ssl
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


def send_email():
    sender_email = "sender email"
    sender_password = "code"
    receiver_email = "receiver email"

    subject = "Жалоба на шантаж и угрозы"
    body = """text"""

    file_path = Path("file")


    if not file_path.exists():
        print(f"❌ Файл не найден: {file_path}")
        print("Программа остановлена.")
        return

    print(" НАЧАТА ОТПРАВКА ЖАЛОБ КАЖДЫЕ 20 МИЛЛИСЕКУНД")
    print(" Для остановки нажмите Ctrl+C")
    print("-" * 50)

    count = 0
    start_time = time.time()

    while True:
        try:
            count += 1

            # Создаем сообщение
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            # Добавляем текст
            message.attach(MIMEText(body, "plain", "utf-8"))

            # Добавляем вложение
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={file_path.name}",
                )
                message.attach(part)


            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=30) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)


            elapsed = time.time() - start_time
            print(f" УСПЕШНО ОТПРАВЛЕНО #{count} | Время: {elapsed:.2f} сек | Отправок/сек: {count / elapsed:.1f}")


            time.sleep(0.01)

        except KeyboardInterrupt:
            elapsed = time.time() - start_time
            print(f"\n Программа остановлена.")
            print(f" Всего отправлено: {count}")
            print(f" Прошло времени: {elapsed:.2f} сек")
            print(f" Средняя скорость: {count / elapsed:.1f} отправок/сек")
            break
        except Exception as e:
            print(f" Ошибка при отправке #{count}: {e}")
            print(" Повтор через 0.02 секунды...")
            time.sleep(0.02)


if __name__ == "__main__":
    send_email()