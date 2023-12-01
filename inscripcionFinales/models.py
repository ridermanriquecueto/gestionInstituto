from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, Group, PermissionsMixin, AbstractUser, User,)
from django.db import models
from django.utils.timezone import now
from .choices import ESTADO_CIVIL_CHOICES,SEXO_CHOICES,MODALIDAD_CHOICES
import random
#from django.contrib.auth.forms import PasswordChangeForm


class UsuarioManager(BaseUserManager):
    
    def create_user(self ,email, password, **extra_fields):
        if not email:
            raise ValueError('Los usuarios deben tener una direccion de email')

        user =self.model(
          email= self.normalize_email(email),
          
        )
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
        
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
          email = self.normalize_email(email),
          password = password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser,PermissionsMixin):
      
    email = models.EmailField('email', max_length=254, unique = True)
    username = models.CharField('username',unique = True,null = True, max_length=100, blank=False)
    nombres = models.CharField('nombres', max_length=200, null=True, blank=True)
    apellidos = models.CharField('apellidos', max_length=200, null=True, blank=True)
    fecha_nac = models.DateField('fecha_nac', null=True, blank=True)
    dni = models.IntegerField('dni',unique = True, null= True, blank=True)
    direccion = models.CharField('direccion', max_length=50, null=True, blank=True)
    localidad = models.CharField('localidad', max_length=50, null=True, blank=True)
    ciudad = models.CharField('ciudad', max_length=100, null=True, blank=True)
    nacionalidad = models.CharField('nacionalidad',max_length=50, null=True, blank=True)
    telefono_1 = models.IntegerField('telefono_1', null=True, blank=True)
    telefono_2 = models.IntegerField('telefono_2', null=True, blank=True)
    estado_civil=models.CharField('estado_civil', choices=ESTADO_CIVIL_CHOICES,max_length=50, null=True, blank=True)
    sexo=models.CharField('sexo',choices=SEXO_CHOICES,max_length=2, null=True, blank=True)
    imagen = models.ImageField('imagenPerfil', upload_to='perfil/', max_length=200, null=True, blank=True)
    is_admin = models.BooleanField('is_admin', default=False)
    is_superuser = models.BooleanField('is_superuser', default=False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    carrera = models.ManyToManyField('Carrera',blank=True)
    Estudiante = 'Estudiante'          
    Preceptor = 'Preceptor'
    Profesor = 'Profesor'
    Directivo = 'Directivo'
    Administrador = 'Administrador'
    

    ROL_CHOICES = (
        (Directivo, 'Directivo'),
        (Preceptor, 'Preceptor'),
        (Profesor, 'Profesor'),
        (Estudiante, 'Estudiante'),
        (Administrador, 'Administrador'),
        
     )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default=Estudiante)
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    
    def __str__(self):
        return self.email

    


class Carrera(models.Model):
    nombre_carrera = models.CharField('nombre_carrera',unique = True, max_length=100)
    num_resolucion = models.CharField('num_resolucion', max_length=100, blank = True, null = True)
    duracion_carrera = models.PositiveBigIntegerField(default=3)
    instituto = models.ForeignKey('Instituto',on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.nombre_carrera
    
    

class usuarios_carreras(models.Model):
    carreras = models.ManyToManyField('Carrera', blank=False)
    usuario= models.ManyToManyField('Usuario', blank=False)
    
class materia_carrera(models.Model):
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, null=True)
    carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE, null=True)

class Instituto(models.Model):
    nombre_instituto = models.CharField('nombre_instituto',unique = True, max_length=100)
    email_instituto = models.EmailField('email_instituto', max_length=254, unique = True)
    direccion=models.CharField('direccion', max_length=50)
    localidad=models.CharField('localidad', max_length=50)
    ciudad=models.CharField('ciudad', max_length=100)
    telefono_1 = models.IntegerField('telefono_1')
    telefono_2 = models.IntegerField('telefono_2')
    
    imagen = models.ImageField('imagenPerfil', upload_to='perfil/', max_length=200,blank = True,null = True)
    
    def __str__(self):
        return self.nombre_instituto


class Materia(models.Model):
    nombre_materia = models.CharField('nombre_materia',unique = True, max_length=30)
    carrera = models.ForeignKey('Carrera',on_delete=models.CASCADE,null=True)
    profesor = models.ForeignKey('Usuario',on_delete=models.CASCADE,null=True)

    Inicio = '12:00'
    Inicio1 = '14:00'
    Inicio2 = '16:00'
    Inicio3 = '18:00'
    Inicio4 = '20:00'
    
    HORARIO_CHOICES = ( 
        (Inicio, '12:00'),
        (Inicio1, '14:00'),
        (Inicio2, '16:00'),
        (Inicio3, '18:00'),
        (Inicio4, '20:00')
        )
    Horario=models.CharField(max_length=22, choices=HORARIO_CHOICES, default=Inicio)   
   
    
    Primero=1
    Segundo=2
    Tercero=3
    ANIO_CHOICES = (
        (Primero, 1),
        (Segundo, 2),
        (Tercero, 3),        
     )
    anio=models.IntegerField(choices=ANIO_CHOICES, default=Primero)
    
    def __str__(self):
        return self.nombre_materia
    


class MateriaCorrelativa(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='materias_correlativas')
    materia_correlativa = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='correlativas_de')

    def __str__(self):
        return f"{self.materia} -> {self.materia_correlativa}"

class usuarios_materia(models.Model):
    materia = models.ForeignKey('Materia',on_delete=models.CASCADE,null=False, blank=False)
    usuario= models.ForeignKey('Usuario',on_delete=models.CASCADE,null=False, blank=False)
    nota_cursada=models.FloatField('Nota de Cursada',null=True,blank=True)
    nota_final=models.FloatField('Nota de Final',null=True,blank=True)
    aprobada= models.BooleanField(default=False)
    modalidad=models.CharField('Modalidad',choices=MODALIDAD_CHOICES,max_length=2, null=True, blank=True)
    ciclo_lectivo=models.CharField('Ciclo lectivo',unique = True,null=True, blank=True, max_length=100)

    def __str__(self):
        return f"{self.materia} -> {self.usuario}"
    
    def puede_inscribirse_en_mesa_final(self):
        return (self.nota_cursada >= 4 or self.modalidad == 'Libre') and self.aprobada == False
    
class MesaFinal(models.Model):
    materia= models.ForeignKey(Materia, on_delete=models.CASCADE, blank=False, null=False )
    llamado= models.DateTimeField('Llamado', null=False, blank=False) 
    vigente= models.BooleanField(default=True) 
    def __str__(self):
        return f"{self.materia} -> {self.llamado}"

class InscripcionFinal(models.Model):
    usuario= models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False, null=False)
    llamado= models.ForeignKey(MesaFinal, on_delete=models.CASCADE, blank=False, null=False)
    aprobada= models.BooleanField(null=True) 


class Estudiante(Usuario):
    matricula= models.CharField(max_length=10,unique=True)

class Profesor(Usuario):
    especialidad = models.CharField(max_length=100)

class Directivo(Usuario):
    cargo = models.CharField(max_length=100)

class Preceptor(Usuario):
    area = models.CharField(max_length=100)
