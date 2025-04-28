#!/usr/bin/env python

marcos_libres = [0x0, 0x1, 0x2]
reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
segmentos = [('.text', 0x00, 0x1A),
             ('.data', 0x40, 0x28),
             ('.heap', 0x80, 0x1F),
             ('.stack', 0xC0, 0x22)]

def procesar(segmentos, reqs, marcos_libres):
    tam_pagina = 16
    memoria_asignada = {}
    cola_fifo = []
    results = []

    for direccion in reqs:
        direccion_valida = False
        for nombre, base, limite in segmentos:
            if base <= direccion < base + limite:
                direccion_valida = True
                break

        # Si la dirección no es válida, se genera un "Segmentation Fault" y se termina la ejecución
        if not direccion_valida:
            results.append((direccion, 0x1FF, "Segmentation Fault"))
            break

        pagina = direccion // tam_pagina
        offset = direccion % tam_pagina

        if pagina in memoria_asignada:
            marco_asignado = memoria_asignada[pagina]
            accion = "Marco ya estaba asignado"
        else:
            if marcos_libres:
                marco_asignado = marcos_libres.pop(0)
                accion = "Marco libre asignado"
            else:
                pagina_salida = cola_fifo.pop(0)
                marco_asignado = memoria_asignada.pop(pagina_salida)
                accion = "Marco asignado"
    
            memoria_asignada[pagina] = marco_asignado
            cola_fifo.append(pagina)

        # Calcular la dirección física
        direccion_fisica = marco_asignado * tam_pagina + offset
        results.append((direccion, direccion_fisica, accion))

    return results



def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Dirección Física: {result[1]:#0{4}x} Acción: {result[2]}")


if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)
