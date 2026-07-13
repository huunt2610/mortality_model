"""Pipeline dữ liệu: raw (UN WPP / GSO) -> ma trận Dxt, Ext trong data/processed.

Chạy:  python -m src.data.make_dataset
Nguồn UN WPP: tải file "Life Tables" (single age) tại
https://population.un.org/wpp/ và đặt vào data/raw/.
"""
import pandas as pd
from src.config import DATA_RAW, DATA_PROCESSED, load_params


def build_matrices(df: pd.DataFrame, sex: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Từ bảng sống dạng dài (age, year, mx, exposure) dựng ma trận tuổi x năm.

    Nếu nguồn không có exposure trực tiếp, ước lượng Ext từ Lx của bảng sống
    và Dxt = mx * Ext (ghi rõ giả định này trong luận văn).
    """
    p = load_params()
    y0, y1 = p["data"]["years"]["start"], p["data"]["years"]["end"]
    sub = df[(df["sex"] == sex) & df["year"].between(y0, y1)]
    Ext = sub.pivot(index="age", columns="year", values="exposure")
    mx = sub.pivot(index="age", columns="year", values="mx")
    Dxt = (mx * Ext).round(2)
    return Dxt, Ext


def main() -> None:
    p = load_params()
    # TODO: thay tên file bằng file WPP thực tế bạn tải về
    df = pd.read_csv(DATA_RAW / "wpp_life_table_vietnam.csv")
    for sex in p["data"]["sexes"]:
        Dxt, Ext = build_matrices(df, sex)
        Dxt.to_csv(DATA_PROCESSED / f"Dxt_{sex}.csv")
        Ext.to_csv(DATA_PROCESSED / f"Ext_{sex}.csv")
        print(f"[ok] {sex}: {Dxt.shape[0]} tuổi x {Dxt.shape[1]} năm")


if __name__ == "__main__":
    main()
