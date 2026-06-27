import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.getGeneri()
        for g in generi:
            self._view._ddGenre.options.append(ft.dropdown.Option(str(g)))
        self._view.update_page()

    def handleCreaGrafo(self, e):

        genere = self._view._ddGenre.value

        if genere is None:
            self._view.create_alert("Seleziona un anno")
            return

        self._model.buildGraph(genere)

        # pulisco la lista risultati
        self._view.txt_result.controls.clear()

        # stampo le info
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi."))

        artista, influenza = self._model.getMaxInfluenza()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi."))
        self._view.txt_result.controls.append(
            ft.Text(f"Artista con maggiore influenza: {artista.Name} (influenza: {influenza})"))

        self._view.txt_result.controls.append(ft.Text("Top 5 archi per peso:"))
        for n1, n2, peso in self._model.getTop5Archi():
            self._view.txt_result.controls.append(
                ft.Text(f"{n1.Name} -> {n2.Name} : peso {peso}"))


        self._view.update_page()

    def handleCammino(self,e):
        pass