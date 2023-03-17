all: run

run-gadesktop-admin:
	cd gadesktop-admin
	pnpm tauri dev
run-gaserver:
	cd gaserver
	python3 app.py

run-gaserver-desktop-client:
	cd gaserver-desktop-client
	go mod tidy
	go run . 

venv_name := venv

ifeq ($(OS), Windows_NT)
venv_exe := .\$(venv_name)\Scripts\activate
else
venv_exe := source ./$(venv_name)/bin/activate
endif

build-gadesktop-admin:
	pnpm build

setup-env:
	cd gaserver
	python3 -m venv $(venv_name)
	$(venv_exe)
	pip3 install -r requirements.txt

  cd ..
  cd gadesktop-admin
  pnpm install

.PHONY: all setup-env build-gadesktop-admin run-gaserver run-gadesktop-admin run update-submodule
