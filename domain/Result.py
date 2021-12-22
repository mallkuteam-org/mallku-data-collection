class Result:
    def __init__(self, link, band, zoom, uuid):
        self.link = link
        self.band = band
        self.zoom = zoom
        self.uuid = uuid
        self.is_downloaded = False
