# Lillith Murasaki 3D

Modelos 3D de mi OC **Lillith Murasaki**, una kitsune de pelo morado con traje de oficina. Personaje y arte por **FeithNoir**.

Sketchfab: https://sketchfab.com/FeithNoir (los enlaces a cada modelo se agregarán después).

![Comparación](lowpoly/comparison.png)

## Modelos

### 1. Low-poly toon (Blender) — `lowpoly/`
- `lillith_lowpoly.blend`: escena completa con shader toon (Shader to RGB + ColorRamp en EEVEE), contorno negro (Solidify invertido), rig de la cola y animación.
- `lillith_lowpoly.glb`: exportación con materiales de color plano y animación (el shader toon y el contorno solo se ven en Blender).
- **3.487 triángulos** (~7.000 contando el contorno al renderizar), 47 piezas: cabeza y cara, pelo con flequillo sobre el ojo derecho, orejas de zorro, cola con punta clara, chaqueta, camisa, falda, medias, tacones, pinza de calavera, lanyard y credencial.
- Colores tomados del sprite original. Pose A, fácil de riggear.
- Animación: balanceo de la cola (bucle de 2 s) y giro de 360° (6 s, 24 fps). Video: [`turntable.mp4`](lowpoly/turntable.mp4).

| Frente | 3/4 | Lado | Espalda |
|---|---|---|---|
| ![](lowpoly/render_front.png) | ![](lowpoly/render_34.png) | ![](lowpoly/render_side.png) | ![](lowpoly/render_back.png) |

### 2. Prueba de TRELLIS (imagen → 3D con IA) — `trellis/`
- `model.glb`: **11.836 triángulos**, con textura. Generado desde el demo gratuito de Hugging Face [`trellis-community/TRELLIS`](https://huggingface.co/spaces/trellis-community/TRELLIS) a partir de un solo dibujo.
- TRELLIS (Microsoft) tiene licencia MIT.

| Frente | 3/4 | Lado | Espalda |
|---|---|---|---|
| ![](trellis/render_bright_front.png) | ![](trellis/render_bright_34.png) | ![](trellis/render_bright_side.png) | ![](trellis/render_bright_back.png) |

## Reconstruir
```bash
blender -b -P lowpoly/build.py      # crea lillith_lowpoly.blend y .glb (las rutas de salida están en el script)
python3 run.py trellis              # vuelve a llamar al demo de TRELLIS (requiere gradio_client)
blender -b -P render.py -- trellis/model.glb trellis/render
```
Herramientas: Blender 4.2.3 LTS, Python, `gradio_client`, Pillow y ffmpeg.

## Limitaciones conocidas
- Low-poly: cuerpo simplificado (piernas delgadas, manos ovaladas), pelo trasero en un solo bloque, flequillo que se ve flotando de lado, cara muy básica, solo la cola tiene rig y las piezas se superponen en vez de unirse (no apto para impresión 3D).
- TRELLIS: mano levantada deformada, la cara es solo la textura del dibujo y la textura se ve borrosa, sin contornos.

## Licencia
- Modelos, renders y arte: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) © FeithNoir (ver `LICENSE`).
- Código (`lowpoly/build.py`, `run.py`, `render.py`, `bright.py`): MIT.

---
**English:** 3D models of my OC Lillith Murasaki: a scripted low-poly toon model made in Blender (3,487 tris, rigged tail and turntable animation) and an image-to-3D test made with TRELLIS (11,836 tris). Character and art by FeithNoir. Models and art are licensed CC BY-SA 4.0; the scripts are MIT. To rebuild the low-poly model, run `blender -b -P lowpoly/build.py`.
