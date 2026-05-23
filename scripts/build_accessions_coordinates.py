from pathlib import Path

import pandas as pd


RAW_EXCEL = Path("data/raw/Datos Cytb y Mc1r Hague y Routman, 2015.xlsx")
OUTPUT_CSV = Path("data/processed/accessions_coordinates.csv")


def dms_to_decimal(value: str) -> float:
    parts = str(value).strip().replace("−", "-").split()
    if len(parts) != 3:
        raise ValueError(f"Invalid DMS coordinate: {value!r}")

    degrees = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    sign = -1 if degrees < 0 else 1
    return sign * (abs(degrees) + minutes / 60 + seconds / 3600)


def main() -> None:
    df = pd.read_excel(RAW_EXCEL, sheet_name="accessions")
    df.columns = [str(column).strip() for column in df.columns]

    output = (
        df[
            [
                "Genbank number",
                "Gene",
                "Genus",
                "Species",
                "Latitude",
                "Longitude",
            ]
        ]
        .dropna(subset=["Genbank number"])
        .rename(
            columns={
                "Genbank number": "id",
                "Gene": "gene",
                "Genus": "genus",
                "Species": "species",
                "Latitude": "latitude_dms",
                "Longitude": "longitude_dms",
            }
        )
    )

    output["id"] = output["id"].str.strip()
    output["gene"] = output["gene"].str.strip()
    output["genus"] = output["genus"].str.strip()
    output["species"] = output["species"].str.strip()
    output["latitude_dms"] = output["latitude_dms"].astype(str).str.strip()
    output["longitude_dms"] = output["longitude_dms"].astype(str).str.strip()
    output["latitude"] = output["latitude_dms"].map(dms_to_decimal)
    output["longitude"] = output["longitude_dms"].map(dms_to_decimal)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT_CSV, index=False, float_format="%.8f")
    print(f"Wrote {len(output)} records to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
