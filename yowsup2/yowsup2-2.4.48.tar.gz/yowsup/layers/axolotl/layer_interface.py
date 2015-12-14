class YowAxolotlLayerInterface(YowLayerInterface):
    def trustIdentity(self, identity):
        self.layer.trustIdentity(identity)
