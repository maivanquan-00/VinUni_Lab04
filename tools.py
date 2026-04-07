from langchain_core.tools import tool

# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
# Giá cả có logic: cuối tuần đắt hơn, hạng cao hơn đắt hơn

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "05:30", "arrival": "07:30", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "14:00", "arrival": "15:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


def format_price(amount: int) -> str:
    """Format số tiền có dấu chấm phân cách: 1.450.000đ"""
    return f"{amount:,.0f}đ".replace(",", ".")


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố đi (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    """
    flights = FLIGHTS_DB.get((origin, destination))

    # Thử tra ngược chiều nếu không tìm thấy
    if flights is None:
        flights = FLIGHTS_DB.get((destination, origin))
        if flights is not None:
            origin, destination = destination, origin

    if flights is None:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    result = f"Các chuyến bay từ {origin} đến {destination}:\n"
    for i, f in enumerate(flights, 1):
        result += (
            f"\n{i}. {f['airline']} | {f['departure']} → {f['arrival']} | "
            f"Hạng: {f['class']} | Giá: {format_price(f['price'])}"
        )
    return result


@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn
    """
    hotels = HOTELS_DB.get(city)
    if hotels is None:
        return f"Không tìm thấy khách sạn tại {city}."

    # Lọc theo giá tối đa
    filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

    if not filtered:
        return (
            f"Không tìm thấy khách sạn tại {city} với giá dưới "
            f"{format_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
        )

    # Sắp xếp theo rating giảm dần
    filtered.sort(key=lambda h: h["rating"], reverse=True)

    result = f"Khách sạn tại {city} (giá dưới {format_price(max_price_per_night)}/đêm):\n"
    for i, h in enumerate(filtered, 1):
        stars = f"{h['stars']} sao"
        result += (
            f"\n{i}. {h['name']} ({stars}) | "
            f"Giá: {format_price(h['price_per_night'])}/đêm | "
            f"Khu vực: {h['area']} | Rating: {h['rating']}/5"
        )
    return result


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    """
    try:
        expense_items = {}
        for item in expenses.split(","):
            item = item.strip()
            if not item:
                continue
            parts = item.split(":")
            if len(parts) != 2:
                return f"Lỗi format: '{item}' không đúng định dạng 'tên:số_tiền'."
            name = parts[0].strip()
            try:
                amount = int(parts[1].strip())
            except ValueError:
                return f"Lỗi: '{parts[1].strip()}' không phải số tiền hợp lệ."
            expense_items[name] = amount

        total_expenses = sum(expense_items.values())
        remaining = total_budget - total_expenses

        result = "Bảng chi phí:\n"
        for name, amount in expense_items.items():
            result += f"  - {name}: {format_price(amount)}\n"
        result += "  ---\n"
        result += f"  Tổng chi: {format_price(total_expenses)}\n"
        result += f"  Ngân sách: {format_price(total_budget)}\n"

        if remaining >= 0:
            result += f"  Còn lại: {format_price(remaining)}"
        else:
            result += f"  Vượt ngân sách {format_price(abs(remaining))}! Cần điều chỉnh."

        return result

    except Exception as e:
        return f"Lỗi khi tính ngân sách: {str(e)}"
