import csv
from statistics import mean

CAPITAL = 10_000_000
FEE = 0.005
FILE = "prices.csv"


def ema(values, period):
    result = []
    alpha = 2 / (period + 1)

    for i, price in enumerate(values):
        if i == 0:
            result.append(price)
        else:
            result.append(
                alpha * price + (1 - alpha) * result[-1]
            )

    return result


def rsi(values, period=14):
    if len(values) <= period:
        return None

    changes = [
        values[i] - values[i - 1]
        for i in range(1, len(values))
    ]

    gains = [max(x, 0) for x in changes]
    losses = [max(-x, 0) for x in changes]

    avg_gain = mean(gains[-period:])
    avg_loss = mean(losses[-period:])

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def main():
    prices = []

    try:
        with open(FILE, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                prices.append(float(row["buy_price"]))
    except FileNotFoundError:
        print("فایل prices.csv پیدا نشد.")
        return
    except (ValueError, KeyError):
        print("اطلاعات فایل قیمت نامعتبر است.")
        return

    if len(prices) < 50:
        print("حداقل 50 قیمت برای تحلیل لازم است.")
        return

    fast = ema(prices, 20)
    slow = ema(prices, 50)
    current_rsi = rsi(prices)

    print("\nگزارش آزمایشی ملی گلد")
    print("آخرین قیمت:", prices[-1])
    print("RSI:", round(current_rsi, 2))
    print("سرمایه فرضی:", CAPITAL, "تومان")
    print("کارمزد فرضی:", FEE * 100, "درصد")

    if fast[-1] > slow[-1] and 30 < current_rsi < 70:
        print("سیگنال: بررسی خرید آزمایشی")
    elif fast[-1] < slow[-1]:
        print("سیگنال: بررسی فروش آزمایشی")
    else:
        print("سیگنال: فعلاً صبر کن")

    print("این تحلیل توصیه قطعی خرید و فروش نیست.")


if __name__ == "__main__":
    main()
