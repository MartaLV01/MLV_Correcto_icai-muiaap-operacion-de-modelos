from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationInfo, Field, field_validator


# DONE -> TODO: clase PrestamoEntrada (BaseModel) con las 6 variables del modelo, con sus rangos (ver enunciado)
#       Debe rechazar campos que no existan.

class PrestamoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid") #prohibo varibles extra
    
    edad: int = Field(ge=18, le=75)
    ingresos_mensuales: float = Field(gt=0)
    importe_prestamo: float = Field(gt=0)
    plazo_meses: int = Field(ge=6, le=84)
    antiguedad_laboral_anios: int = Field(ge=0, le=50)
    impagos_previos: int = Field(ge=0, le=20)

    # DONE -> TODO: field_validator (con classmethod) para antiguedad_laboral_anios: no puede ser incoherente con la edad.
    # con "before" se hacen estas comprobaciones antes de  pasar el contrato
    # con "after" primero el contrato y luego las comprobaciones
    @field_validator("antiguedad_laboral_anios", mode="after")
    @classmethod
    def verificar_edad(cls, antiguedad_laboral_anios, info: ValidationInfo):
        # Tambien se podria hacer usando self
            #def verificar_edad(self):
            #   if self.antiguedad_laboral_anios > self.edad - 16:
            #   ....
            #return self

        # info -> contiene información adicional sobre la validación
        # info.data -> contiene los campos que Pydantic ya ha validado, 
        #   ya que los hemos validado antes de entrar en esta funcion
        # hay que tener cuidado ya que esto solo funciona cuando
        # los campos que necesitas han sido validados con anterioridad!
        
        #edad = info.data["edad"]
        #if antiguedad_laboral_anios > edad - 16:
        #    raise ValueError("La antigüedad laboral no puede ser mayor que la edad menos 16 años")
        # Al hacer directamente la comprobacion de antiguedad_laboral_anios si la edad no es valida va a dar
        # error (el test test_schemas.py::test_edad_fuera_de_rango fallaba, cuando deberia pasar) 
        # al intentar acceder al campo de infor.data["edad"], ya que este no existe porque no
        # ha pasado la validacion. Por eso veo primero si existe o no.
        if "edad" in info.data:
            edad = info.data["edad"]
            if antiguedad_laboral_anios > edad - 16:
                raise ValueError(
                    "La antigüedad laboral no puede ser mayor que la edad menos 16 años"
                )

        return antiguedad_laboral_anios
        


"""
edad	entero	de 18 a 75
ingresos_mensuales	decimal	mayor que 0
importe_prestamo	decimal	mayor que 0
plazo_meses	entero	de 6 a 84
antiguedad_laboral_anios	entero	de 0 a 50, y no puede ser mayor que (edad - 16) -hacer filedvalidator la antiguedad no puede ser mayor que tu edad!!!!
impagos_previos	entero	de 0 a 20
"""

# DONE -> TODO: clase PrediccionSalida con probabilidad_impago (entre 0 y 1) y decision (aprobar, revisar o rechazar).
class PrediccionSalida(BaseModel):
    probabilidad_impago: float= Field(ge=0, le=1)
    decision: Literal["aprobar", "revisar", "rechazar"]
