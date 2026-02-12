import tkinter as tk
from PIL import Image, ImageTk


def load_image(path, size=None):
    """Безопасная загрузка изображения с обработкой ошибок"""
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        return None


def create_menu_button(parent, text, icon_img, active=False):
    """Создание элемента бокового меню"""
    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="x", pady=2)

    bg_color = "#e7f3ff" if active else "white"
    btn_frame = tk.Frame(frame, bg=bg_color)
    btn_frame.pack(fill="x")

    if icon_img:
        icon_label = tk.Label(btn_frame, image=icon_img, bg=bg_color)
        icon_label.pack(side="left", padx=16, pady=12)
        icon_label.image = icon_img

    label = tk.Label(
        btn_frame,
        text=text,
        font=("Helvetica", 14),
        fg="#0078ff" if active else "#111111",
        bg=bg_color,
        anchor="w"
    )
    label.pack(side="left", pady=12)

    def on_enter(e, f=btn_frame):
        if not active:
            f.config(bg="#f0f7ff")

    def on_leave(e, f=btn_frame):
        if not active:
            f.config(bg="white")

    btn_frame.bind("<Enter>", on_enter)
    btn_frame.bind("<Leave>", on_leave)


main_title = "Мессенджер"


# Константы и пути
LOGO_PATH = 'icons/logo.png'
PROFILE_PHOTO_PATH = 'icons/profile1.png'

AD_IMAGE_PATHS = [
    'icons/ad1.png',
    'icons/ad2.png',
]

ICON_SIZE = (34, 34)


def main():
    root = tk.Tk()
    root.title(main_title)
    root.geometry("1423x997")
    root.configure(bg="#f0f2f5")


    # =====================================
    #   Подготовка иконок меню
    # =====================================
    menu_icons = {
        "Профиль":   "profile",
        "Лента":     "feed",
        "Друзья":    "friends",
        "Мессенджер": "chat",
        "Аватар":    "profile1",  # пока не используется в меню
    }

    icons = {}
    for text, icon_name in menu_icons.items():
        icons[text] = load_image(f"icons/{icon_name}.png", ICON_SIZE)

    # =====================================
    #   ВЕРХНЯЯ ПАНЕЛЬ (Header)
    # =====================================
    header = tk.Frame(root, bg="white", height=60, bd=1, relief="solid")
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    # Логотип + название
    logo_frame = tk.Frame(header, bg="white")
    logo_frame.pack(side="left", padx=16, pady=10)

    logo_img = load_image(LOGO_PATH, (356, 62))
    if logo_img:
        tk.Label(logo_frame, image=logo_img, bg="white").pack(side="left")
        logo_frame.image = logo_img
    else:
        tk.Label(logo_frame, text="M", font=("Helvetica", 24, "bold"),
                 bg="#0078ff", fg="white", width=2).pack(side="left")

    # Поле поиска
    search_frame = tk.Frame(header, bg="white")
    search_frame.pack(side="left", fill="x", expand=True, padx=40)

    tk.Entry(
        search_frame,
        font=("Helvetica", 14),
        bg="#f0f2f5",
        relief="flat",
        bd=0
    ).pack(fill="x", ipady=8, padx=20)

    # Профиль пользователя
    profile_frame = tk.Frame(header, bg="white")
    profile_frame.pack(side="right", padx=16)

    tk.Label(
        profile_frame,
        text="Нечаев",
        font=("Helvetica", 24, "bold"),
        bg="white"
    ).pack(side="left", padx=8)

    profile_img = load_image(PROFILE_PHOTO_PATH, (62, 62))
    if profile_img:
        tk.Label(profile_frame, image=profile_img, bg="white").pack(side="left")
        profile_frame.image = profile_img

    # =====================================
    #   ОСНОВНОЙ КОНТЕЙНЕР
    # =====================================
    main_container = tk.Frame(root, bg="#f0f2f5")
    main_container.pack(fill="both", expand=True)

# Левая панель навигации
    left_sidebar = tk.Frame(main_container, bg="white", width=240, bd=1, relief="solid")
    left_sidebar.pack(side="left", fill="y")
    left_sidebar.pack_propagate(False)

    menu_items = ["Профиль", "Лента", "Друзья", "Мессенджер"]

    for text in menu_items:
        create_menu_button(left_sidebar, text, icons.get(text), active=(text == "Лента"))

    # =====================================
    #   ЦЕНТРАЛЬНАЯ ЧАСТЬ — ГЛАВНАЯ ЛЕНТА
    # =====================================
    feed_container = tk.Frame(main_container, bg="#f0f2f5")
    feed_container.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # Заголовок ленты
    feed_header = tk.Frame(feed_container, bg="#f0f2f5", height=60)
    feed_header.pack(fill="x", pady=(0, 20))
    feed_header.pack_propagate(False)

    tk.Label(
        feed_header,
        text="Главная лента",
        font=("Helvetica", 24, "bold"),
        bg="#f0f2f5",
        fg="#111111"
    ).pack(anchor="w", padx=10, pady=10)

    # Область для постов (пока пустая)
    posts_container = tk.Frame(feed_container, bg="white", bd=1, relief="solid")
    posts_container.pack(fill="both", expand=True)

    # =====================================
    #   ПРАВАЯ ПАНЕЛЬ — РЕКЛАМА
    # =====================================
    right_sidebar = tk.Frame(main_container, bg="white", width=320, bd=1, relief="solid")
    right_sidebar.pack(side="right", fill="y")
    right_sidebar.pack_propagate(False)

    ads_container = tk.Frame(right_sidebar, bg="white")
    ads_container.pack(fill="both", expand=True)

    # Показываем максимум 2 рекламы
    ads_to_show = min(2, len(AD_IMAGE_PATHS))

    for i in range(ads_to_show):
        ad_path = AD_IMAGE_PATHS[i]
        ad_item = tk.Frame(ads_container, bg="white",
                           bd=1 if i < ads_to_show - 1 else 0,
                           relief="solid", padx=20, pady=20)
        ad_item.pack(fill="x", pady=0)

        ad_img = load_image(ad_path, (255, 354))
        if ad_img:
            label = tk.Label(ad_item, image=ad_img, bg="white")
            label.pack(pady=(0), anchor="center")
            label.image = ad_img

    root.mainloop()


if __name__ == "__main__":
    main()