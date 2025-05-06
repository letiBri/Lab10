import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._ddCountryValue = None

    def handleCalcola(self, e):
        self._view._txt_result.controls.clear()
        anno = self._view._txtAnno.value
        if anno == "" or anno is None:
            self._view.create_alert("Inserire un anno!")
            self._view.update_page()
            return
        try:
            annoInt = int(anno)  # lo metto dentro un blocco try perchè questa operazione potrebbe scatenare un errore se non è davvero un numero sottoforma di stringa
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view.create_alert("Inserire un valore intero!")
            self._view.update_page()
            return
        if annoInt > 2006 or annoInt < 1816:
            self._view._txt_result.controls.clear()
            self._view.create_alert("Inserire un anno compreso fra 1816 e 2006!")
            self._view.update_page()
            return
        grafo, lista, numeroCompConnesse = self._model.buildGraph(annoInt)
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {numeroCompConnesse} componenti connesse"))
        self._view._txt_result.controls.append(ft.Text("Di seguito il dettaglio sui nodi: "))
        for stato in lista:
            self._view._txt_result.controls.append(ft.Text(f"{stato}"))
        self._view._ddStato.disabled = False
        self._view._btnRaggiungibili.disabled = False
        self.fillDDStato(grafo)
        self._view.update_page()
        return

    def fillDDStato(self, grafo):
        for node in grafo.nodes:
            self._view._ddStato.options.append(ft.dropdown.Option(key=node.CCode, text=node.StateNme, data=node, on_click=self.readStates))
            self._view._ddStato.options.sort(key=lambda x: x.data.StateNme)

    def readStates(self, e):
        self._ddCountryValue = e.control.data

    def handleRaggiungibili(self, e):
        self._view._txt_result.controls.clear()
        statoScelto = self._ddCountryValue
        if statoScelto is None:
            self._view.create_alert("Inserire un stato!")
            self._view.update_page()
            return
        listaRaggiungibili, lunghezza = self._model.getNodiRaggiungibili(statoScelto)
        if lunghezza == 0:
            self._view._txt_result.controls.append(ft.Text(f"Non ci sono stati raggiungibili, probabilmente hai selezionato un'isola!"))
            self._view.update_page()
            return
        self._view._txt_result.controls.append(ft.Text(f"I nodi raggiungibili da {statoScelto} sono {lunghezza}:"))
        for state in listaRaggiungibili:
            self._view._txt_result.controls.append(ft.Text(f"{state}"))
        self._view.update_page()
        return

