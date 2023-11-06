class TankSkinManager:
    def __init__(self):
        self.tank_sprite = 1
        self.skin_paths = ["assets/tank1.png", "assets/tank2.png", "assets/tank3.png"]
        self.current_skin_path = self.skin_paths[self.tank_sprite - 1]

    def get_current_skin_path(self):
        return self.current_skin_path

    def next_skin(self):
        self.tank_sprite = (self.tank_sprite % 3) + 1
        self.current_skin_path = self.skin_paths[self.tank_sprite - 1]