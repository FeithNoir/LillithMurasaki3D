# Lillith Murasaki 3D

Modelos 3D de mi OC **Lillith Murasaki**, una kitsune de pelo morado con traje de oficina. Personaje y arte por **FeithNoir**.

Sketchfab: https://sketchfab.com/FeithNoir (los enlaces a cada modelo se agregarán después).

![Comparación](lowpoly/comparison.png)

## Versiones
| Versión | Carpeta | Triángulos | Rig | Animaciones |
|---|---|---|---|---|
| Low-poly v1 | `lowpoly/` | 3.487 | Solo cola | Cola + giro 360° |
| Low-poly v2 | `lowpoly_v2/` | 4.915 | 34 huesos (Humanoid) | Idle, Wave, Walk, TailSway |
| TRELLIS (IA) | `trellis/` | 11.836 | No | No |
| TRELLIS v2 (IA, limpio) | `trellis_v2/` | ~24.000 | 34 huesos (igual que Low-poly v2) | Idle, Wave, Walk, TailSway |

### Escenarios
| Escenario | Carpeta | Triángulos | Objetos |
|---|---|---|---|
| Oficina low-poly | `office/` | ~1.250 | 97 |

Perfil de Sketchfab: https://sketchfab.com/FeithNoir

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

### 2. Low Poly v2 (con rig) — `lowpoly_v2/`
La v1 se conserva intacta en `lowpoly/`; la v2 vive aparte.

![Comparación v1 vs v2](lowpoly_v2/comparison_v2.png)

- `lillith_lowpoly_v2.blend` y `lillith_lowpoly_v2.glb`: **4.915 triángulos**, 55 piezas.
- **Esqueleto de 34 huesos** con nombres estilo Unity Humanoid (.L/.R): Root, Hips, Spine, Chest, Neck, Head; Shoulder/UpperArm/LowerArm/Hand L/R; UpperLeg/LowerLeg/Foot/Toes L/R; Ear L/R; HairBack.0-2, SideLock L/R; Tail.0-4.
- Pelo lateral más lleno y tacones de salón (pump) con tacón cuadrado.
- Animaciones incluidas en el GLB: **Idle** (bucle de 3 s), **Wave** (2 s), **Walk** (bucle de 1 s) y **TailSway** (bucle de 2 s). Videos: [`turntable_v2.mp4`](lowpoly_v2/turntable_v2.mp4), [`anim_preview_v2.mp4`](lowpoly_v2/anim_preview_v2.mp4).
- Reconstruir: `blender -b -P lowpoly_v2/build_v2.py`. Nota: algunos scripts auxiliares (`build_v2.py`, `render_v2.py`, `test_v2.py`) usan rutas de mi entorno de trabajo (`/workspace/lillith-3d`); ajústalas antes de ejecutarlos.

![Frente v2](lowpoly_v2/render_front_v2.png)

| Frente | 3/4 | Lado | Espalda |
|---|---|---|---|
| ![](lowpoly_v2/render_front_v2.png) | ![](lowpoly_v2/render_34_v2.png) | ![](lowpoly_v2/render_side_v2.png) | ![](lowpoly_v2/render_back_v2.png) |

**Limitaciones conocidas (v2):** la caminata es rígida y los pies se deslizan, la falda atraviesa las piernas en pasos amplios, no hay huesos de dedos, y el shader toon y el contorno solo se ven dentro de Blender.

### 3. Prueba de TRELLIS (imagen → 3D con IA) — `trellis/`
- `model.glb`: **11.836 triángulos**, con textura. Generado desde el demo gratuito de Hugging Face [`trellis-community/TRELLIS`](https://huggingface.co/spaces/trellis-community/TRELLIS) a partir de un solo dibujo.
- TRELLIS (Microsoft) tiene licencia MIT.

| Frente | 3/4 | Lado | Espalda |
|---|---|---|---|
| ![](trellis/render_bright_front.png) | ![](trellis/render_bright_34.png) | ![](trellis/render_bright_side.png) | ![](trellis/render_bright_back.png) |

### 4. TRELLIS v2 (limpio, con rig) — `trellis_v2/`
Versión mejorada del modelo generado con TRELLIS (imagen → 3D, MIT), limpiada y remallada.
- `lillith_trellis_v2.blend` / `lillith_trellis_v2.glb`: ~24k triángulos, 1,65 m de altura.
- `lillith_trellis_v2_albedo.png`: textura horneada de 2048 px.
- Manos nuevas de 5 dedos y rostro proyectado desde el sprite.
- Mismo rig de 34 huesos que Low-poly v2, con animaciones Idle, Wave, Walk y TailSway.
- Renders (`render_front/34/side/back.png`), `comparison.png`, `turntable.mp4`, `anim_preview.mp4` y scripts (`build.py`, `render.py`, `test.py`, `look.py`, `grid.py`).

Limitaciones: el rostro se estira a partir de unos 45°; queda una segunda copia borrosa del cráneo detrás de la oreja; la textura es suave lejos de la cara; hay pliegues en la cola y la caminata es rígida. Es un modelo derivado de generación con IA (TRELLIS, licencia MIT).

### 5. Oficina low-poly (escenario) — `office/`
Oficina de Lillith en low-poly basada en `office_bg.png`, construida por script con primitivas en Blender.
- `lillith_office.blend` / `lillith_office.glb`: unos 1.250 triángulos y 97 objetos.
- El look toon y el contorno solo se ven en Blender; el `.glb` lleva los materiales base.
- Renders: `render_ref_view.png`, `render_wide_34.png`, `render_with_lillith.png` y `comparison.png`; script `build.py`.

Limitaciones: la ciudad exterior se ve como bloques oscuros, no hay haces de luz ni vidrio, y el encuadre de la cámara respecto a la referencia es aproximado.

## Reconstruir
```bash
blender -b -P lowpoly_v2/build_v2.py  # v2 con rig y animaciones
blender -b -P lowpoly/build.py      # crea lillith_lowpoly.blend y .glb (las rutas de salida están en el script)
python3 run.py trellis              # vuelve a llamar al demo de TRELLIS (requiere gradio_client)
blender -b -P render.py -- trellis/model.glb trellis/render
```
Herramientas: Blender 4.2.3 LTS, Python, `gradio_client`, Pillow y ffmpeg.

## Limitaciones conocidas
- Low-poly v1: cuerpo simplificado (piernas delgadas, manos ovaladas), pelo trasero en un solo bloque, flequillo que se ve flotando de lado, cara muy básica, solo la cola tiene rig y las piezas se superponen en vez de unirse (no apto para impresión 3D).
- TRELLIS: mano levantada deformada, la cara es solo la textura del dibujo y la textura se ve borrosa, sin contornos.

## Licencia
- Modelos, renders y arte: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) © FeithNoir (ver `LICENSE`).
- Código (`lowpoly/build.py`, `run.py`, `render.py`, `bright.py`, `lowpoly_v2/*.py`): MIT.

---
**English:** 3D models of my OC Lillith Murasaki: a scripted low-poly toon model made in Blender (3,487 tris, rigged tail and turntable animation) and an image-to-3D test made with TRELLIS (11,836 tris). Character and art by FeithNoir. Models and art are licensed CC BY-SA 4.0; the scripts are MIT. To rebuild the low-poly model, run `blender -b -P lowpoly/build.py`. **v2** (`lowpoly_v2/`): 4,915 tris, 34-bone Humanoid-style rig, fuller side hair, block-heel pumps, and Idle/Wave/Walk/TailSway animations in the GLB; rebuild with `blender -b -P lowpoly_v2/build_v2.py` (helper scripts reference local `/workspace/lillith-3d` paths).
