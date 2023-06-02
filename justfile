default:
  just --list

install:
  poetry install

package:
  poetry build
