import sys
import subprocess
import platform

COMPOSE_FILE = "docker-compose.dev.yml"
BACKEND_SERVICE = "backend"
DB_CONTAINER_NAME = "gen-canvas-db"
DB_USER = "DevUser"
DB_NAME = "gen_canvas_db"


def run_command(command_list):
    """Chạy lệnh subprocess an toàn đa nền tảng."""
    try:
        is_windows = platform.system() == "Windows"
        subprocess.run(command_list, shell=is_windows, check=True)
    except subprocess.CalledProcessError:
        print(f"\nLệnh thất bại: {' '.join(command_list)}")
    except KeyboardInterrupt:
        print("\nĐã dừng lệnh thủ công.")


def compose_up():
    print("\nĐang build & start container (dev mode)...")
    run_command(["docker", "compose", "-f", COMPOSE_FILE, "up", "--build"])


def compose_down():
    print("\nDừng và xóa container...")
    run_command(["docker", "compose", "-f", COMPOSE_FILE, "down"])


def compose_restart():
    print(f"\nRestart nhanh container {BACKEND_SERVICE}...")
    run_command(["docker", "compose", "-f", COMPOSE_FILE, "restart", BACKEND_SERVICE])


def compose_logs():
    print(f"\nĐang theo dõi logs {BACKEND_SERVICE} (Ctrl+C để thoát)...")
    try:
        run_command(["docker", "compose", "-f", COMPOSE_FILE, "logs", "-f", BACKEND_SERVICE])
    except KeyboardInterrupt:
        pass


def open_db_shell():
    print(f"\n🗄Mở shell PostgreSQL trong container `{DB_CONTAINER_NAME}`...")
    print(f"   (User: {DB_USER}, DB: {DB_NAME}) - Gõ '\\q' hoặc 'exit' để thoát.")
    run_command([
        "docker", "exec", "-it", DB_CONTAINER_NAME,
        "psql", "-U", DB_USER, "-d", DB_NAME
    ])


def clean_system():
    print("\nDọn dẹp hệ thống Docker (Prune images/containers rác)...")
    run_command(["docker", "system", "prune", "-f"])


def show_menu():
    while True:
        print("\n" + "=" * 45)
        print("      GEN CANVAS DEV TOOLS       ")
        print("=" * 45)
        print("  1. UP      (Build & Start Stack)")
        print("  2. DOWN    (Stop & Remove Stack)")
        print("  3. RESTART (Restart Backend)")
        print("  4. LOGS    (View Backend Logs)")
        print("  5. DB      (Access PostgreSQL Shell)")
        print("  6. CLEAN   (Docker System Prune)")
        print("  0. EXIT")
        print("=" * 45)

        choice = input("Chọn chức năng (0-6): ").strip()

        if choice == "1":
            compose_up()
        elif choice == "2":
            compose_down()
        elif choice == "3":
            compose_restart()
        elif choice == "4":
            compose_logs()
        elif choice == "5":
            open_db_shell()
        elif choice == "6":
            clean_system()
        elif choice == "0":
            print("Bye bye!")
            break
        else:
            print("Lựa chọn không hợp lệ!")

        if choice != "4" and choice != "5":
            input("\n(Nhấn Enter để tiếp tục...)")

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "up":
            compose_up()
        elif cmd == "down":
            compose_down()
        elif cmd == "restart":
            compose_restart()
        elif cmd == "logs":
            compose_logs()
        elif cmd == "db":
            open_db_shell()
        elif cmd == "clean":
            clean_system()
        else:
            print(f"Lệnh không tồn tại: {cmd}")
            print("Chạy không tham số để mở Menu.")
    else:
        show_menu()


if __name__ == "__main__":
    main()