import atmos.moisture as moisture
import atmos.thermo as thermo


def main():
    p = 100000.0
    T = 303.15
    RH = 0.6

    q = moisture.specific_humidity_from_relative_humidity(p, T, RH)

    Tw_pseudo = thermo.wet_bulb_temperature(p, T, q, saturation="pseudo")
    Tw_isobaric = thermo.wet_bulb_temperature(p, T, q, saturation="isobaric")

    Tw_pseudo_c = float(Tw_pseudo - 273.15)
    Tw_isobaric_c = float(Tw_isobaric - 273.15)

    print("Wet-bulb temperature example (湿球温度示例)")
    print(f"Pressure: {p/100:.0f} hPa")
    print(f"Air temperature: {T-273.15:.1f} °C")
    print(f"Relative humidity: {RH*100:.0f} %")
    print(f"Pseudo wet-bulb temperature: {Tw_pseudo_c:.2f} °C")
    print(f"Isobaric wet-bulb temperature: {Tw_isobaric_c:.2f} °C")


if __name__ == "__main__":
    main()
