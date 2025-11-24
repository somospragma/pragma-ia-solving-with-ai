# Function Call Cycle Detection\n\n
## REGLA: cycle_detection\n- **Lenguajes soportados**: java, py\n- **Descripcion**: Detecta ciclos en la cadena de llamadas entre funciones o metodos. Si path_code esta definido, obten el codigo de esa ubicacion, caso contrario solicita al usuario que proporcione el codigo a analizar.\n\n
## CODIGO A ANALIZAR:\nObtener codigo desde: s3://{bucket}/{key}\n\n
## NOTIFICACION POST-ANALISIS:\nDespues del analisis, notificar a: architecture@pragma.com\nMensaje: Se detectaron ciclos en las llamadas de funciones.\n\n
## FORMATO DE SALIDA REQUERIDO:\n```json\n[{\"ciclo_detectado\": boolean, \"funciones_involucradas\": [{\"clase\": \"string\", \"funcion\": \"string\", \"linea_inicio\": number}], \"mensaje\": \"string\"}]\n```\n\n
## INSTRUCCIONES:\nEjecuta el analisis segun la regla especificada y proporciona resultados en el formato JSON indicado.