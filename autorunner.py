import subprocess
import time
import random
from colorama import Fore, init
import telebot


TARGET_SCRIPT = "accs_changer.py"

BOT_TOKEN = "___"
USER_ID = 123

bot = telebot.TeleBot(BOT_TOKEN)


def notify_user(text: str):
    try:
        bot.send_message(USER_ID, text)
    except Exception as e:
        print(f"{Fore.RED}[NOTIFY ERROR]{Fore.RESET} {e}")


def run_file(target_script, run_number):
    try:
        result = subprocess.run(["python", target_script], capture_output=True, text=True)

        if result.returncode == 0:
            msg = f"✅ Запуск №{run_number} успешно выполнен."

            print(f"{Fore.GREEN}[SUCCESS]{Fore.RESET} Запуск №{Fore.LIGHTBLUE_EX}{run_number}{Fore.RESET} успешно выполнен.")
            notify_user(msg)
            return True, False
        else:
            msg = f"❌ Запуск №{run_number} завершился с ошибкой. Код: {result.returncode}"

            print(f"{Fore.RED}[ERROR]{Fore.RESET} Запуск №{Fore.LIGHTBLUE_EX}{run_number}{Fore.RESET} завершился с ошибкой.")
            print("Код ошибки:", result.returncode)
            if result.stderr:
                print("Вывод stderr:\n", result.stderr)
                msg += f"\nstderr:\n{result.stderr}"
            notify_user(msg)
            return False, False

    except Exception as e:
        msg = f"💥 Критическая ошибка при запуске subprocess: {e}"
        print(f"{Fore.RED}[CRITICAL ERROR]{Fore.RESET} Критическая ошибка при запуске subprocess:")
        print(str(e))
        notify_user(msg)
        return False, True


def main():
    success_count = 0
    error_count = 0
    total_minutes = 0
    run_number = 0

    print(f"{Fore.CYAN}[INFO]{Fore.RESET} Скрипт запущен. Целевой файл: {TARGET_SCRIPT}")

    while True:
        run_number += 1
        delay = random.randint(45, 60)
        total_minutes += delay

        print(f"{Fore.WHITE}[WAIT] Следующий запуск через {delay} минут...")
        time.sleep(delay * 60)

        print(f"{Fore.YELLOW}[START]{Fore.RESET} Запуск №{run_number}...")

        success, fatal = run_file(TARGET_SCRIPT, run_number)

        if success:
            success_count += 1
        else:
            error_count += 1

        print(f"{Fore.CYAN}Время работы: {total_minutes} минут | Успехов: {success_count} | Ошибок: {error_count}{Fore.RESET}")

        if fatal:
            print(f"{Fore.RED}[STOP]{Fore.RESET} Работа остановлена из-за критической ошибки.")
            break


if __name__ == "__main__":
    init(autoreset=True)
    main()
    input("Нажмите Enter для выхода... ")