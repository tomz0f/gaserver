website:
	python3 app.py
desktop:
	python3 galbul-desktop.py
admin: gadesktop-admin
	cd gadesktop-admin && pnpm install && pnpm electron-dev
	cd ..
