from threading import Thread
from website import create_app
from application import wimchacker

DEBUG=True
app = create_app()

def run_webApp():
    app[0].run(debug=False)

if __name__ == '__main__':

    if not DEBUG:
        thread = Thread(target=run_webApp)
        thread.start()
        with app[0].app_context():
            wimchacker.app = app[0]
            wimchacker.db = app[1]
            wimchacker.run()
    else:
        app[0].run(debug=True)







# import win32serviceutil
# import win32service
# import win32event
# import servicemanager
# import os.path
# import sys
#
# # Funkcja do łączenia się z serwerami
# def connect_to_servers():
#     # Tu umieść swój kod odpowiedzialny za łączenie się z serwerami.
#     pass
#
# # Kod aplikacji Flask.
# from website import create_app
# app = create_app()
#
#
# # Klasa reprezentująca usługę Windows.
# class MyService(win32serviceutil.ServiceFramework):
#     # Nazwa wewnętrzna usługi.
#     _svc_name_ = 'MyFlaskWMI'
#     # Wyświetlana nazwa usługi.
#     _svc_display_name_ = 'My Flask and WMI Service'
#
#     def __init__(self, args):
#         # Inicjalizacja klasy bazowej.
#         win32serviceutil.ServiceFramework.__init__(self, args)
#         # Utworzenie zdarzenia służącego do zatrzymania usługi.
#         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
#         self.is_alive = True
#
#     def SvcStop(self):
#         # Metoda wywoływana, gdy usługa ma zostać zatrzymana.
#         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#         # Zmiana stanu flagi w celu zakończenia głównej pętli usługi.
#         self.is_alive = False
#
#     def SvcDoRun(self):
#         # Metoda wywoływana podczas uruchamiania usługi.
#         # Logowanie rozpoczęcia usługi do dziennika zdarzeń systemu Windows.
#         servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                               servicemanager.PYS_SERVICE_STARTED,
#                               (self._svc_name_, ''))
#         # Rozpoczęcie głównej pętli usługi.
#         self.main()
#
#     def main(self):
#         # Sprawdzenie, czy plik WMI.db istnieje.
#         if os.path.exists("WMI.db"):
#             # Jeśli istnieje, próbuj połączyć się z serwerami.
#             connect_to_servers()
#         # Uruchom aplikację Flask.
#         #app.run(host='0.0.0.0', port=5000)
#         app.run(debug=False)
#
# if __name__ == '__main__':
#     # Kod uruchamiany podczas wywoływania skryptu.
#     # Jeśli skrypt został uruchomiony bez argumentów, inicjalizuj usługę i uruchom ją.
#     if 'debug' in sys.argv:
#         # Jeśli uruchamiasz skrypt z argumentem "debug", uruchomi funkcję main() bezpośrednio.
#         MyService(['MyFlaskWMI']).main()
#     elif len(sys.argv) == 1:
#         servicemanager.Initialize()
#         servicemanager.PrepareToHostSingle(MyService)
#         servicemanager.StartServiceCtrlDispatcher()
#     else:
#         # W przeciwnym razie przetwarzaj argumenty linii poleceń (np. install, start).
#         win32serviceutil.HandleCommandLine(MyService)