class Cliente:
    def __init__(self, cedula, nombre, apellido, fec_nacimiento, telefono, correo_electronico):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.fec_nacimiento = fec_nacimiento
        self.telefono = telefono
        self.correo_electronico = correo_electronico

    def to_dict(self):
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fec_nacimiento": self.fec_nacimiento,
            "telefono": self.telefono,
            "correo_electronico": self.correo_electronico
        }

    def __str__(self):
        return f"Cliente({self.cedula}, 
        {self.nombre}, {self.apellido}, 
        {self.fec_nacimiento}, {self.telefono}, 
        {self.correo_electronico})"