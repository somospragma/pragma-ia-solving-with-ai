Debes realizar los test unitarios del componente (#nombre-componente.tsx). 

Sigue las intrucciones a continuación para crear los test unitarios:

- El archivo de test debe tener el mismo nombre que el componente pero con la extensión .test.tsx. En caso de que no exista el archivo en el proyecto crealo, si ya existe modificalo pero no elimines nada de su contenido, solo amplialo. 
- No pruebes estilos, accesibilidad, diseño responsibe, integración de los componentes ni otras aspectos que no tengan que ver con la lógica de ejecución y renderización.
- Manten los test simples, haz la menor cantidad de test posibles para garantizar un cobertura de (% de cobertura deseado) de los escenarios de prueba. Ten en cuenta las siguientes recomendaciones:
  - Cubre los casos y error más comunes.
  - El tamaño máximo del archivo de test será de 300 lineas de código.
  - No agregues comentarios innecesarios en el código de test.
  - Prioriza la legibilidad y mantenibilidad del código de test.
  - No uses snapshots en los test. (Según proyecto)
- Asegúrate de importar todo lo necesario en el archivo de test. Usa mocks para las dependencias externas y funciones asíncronas. 
  - Usa las librerías para los test que se tengan previamente instaladas en el proyecto y que se implementen en otros archivos de test para mantener la coherencia y reutilización.
  - No instales ninguna librería adicional sin autorización.
- Usa descripciones claras y concisas para cada nombre de test y las variables creadas en cada uno de ellos.
- Asegúrate de que los test sean independientes entre sí.
- Usa el formato de otras pruebas ya existentes en el proyecto como referencia para mantener la coherencia en el estilo de los test.