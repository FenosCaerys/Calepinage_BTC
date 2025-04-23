#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de calepinage pour les Blocs de Terre Comprimée (BTC)

Cette application permet de calculer et visualiser le calepinage
d'un mur construit en BTC en fonction de ses dimensions.
"""

import sys
from PyQt5.QtWidgets import QApplication
from btc_gui import BTCCalepineur


def main():
    """Point d'entrée principal de l'application"""
    app = QApplication(sys.argv)
    window = BTCCalepineur()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
