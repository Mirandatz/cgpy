import cgpy.colors as cc
import cgpy.devices as cd


def main() -> None:
    device = cd.Device(num_rows=60, num_columns=80)
    palettes = [
        [cc.Color.from_ints(128, 0, 211)],  # roxo claro
        [cc.Color.from_ints(75, 0, 130)],  # roxo escuro
        [cc.Color.from_ints(0, 0, 25)],  # azul
        [cc.Color.from_ints(0, 255, 0)],  # verde
        [cc.Color.from_ints(255, 255, 0)],  # amarelo
        [cc.Color.from_ints(255, 127, 0)],  # laranja
        [cc.Color.from_ints(255, 0, 0)],  # vermelho
    ]

    cd.animate_devices(
        devices=[device] * 7,
        palettes=palettes,
        fps=60,
    )


if __name__ == "__main__":
    main()
