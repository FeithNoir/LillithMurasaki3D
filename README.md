# Lillith Murasaki 3D

Modelos 3D de mi OC **Lillith Murasaki**, una kitsune de pelo morado con traje de oficina. Personaje y arte por **FeithNoir**.

Sketchfab: https://sketchfab.com/FeithNoir (los enlaces a cada modelo se agregarán después).

![Comparación](lowpoly/comparison.png)

## Versiones
| Versión | Carpeta | Triángulos | Rig | Animaciones |
|---|---|---|---|---|
| Low-poly v1 | `lowpoly/` | 3.487 | Solo cola | Cola + giro 360° |
| Low-poly v2 | `lowpoly_v2/` | 4.915 | 34 huesos (Humanoid) | Idle, Wave, Walk, TailSway |
| Low-poly v3 (expresiones) | `lowpoly_v3/` | 5.051 | 34 huesos (igual que v2) | Idle (con parpadeo), Wave, Walk, TailSway, Expressions |
| Low-poly v4 (final) | `lowpoly_v4/` | 6.405 | 34 huesos (igual que v2) | Idle, Wave, Walk, TailSway, Expressions, Sit, ChairSpin |
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
### 6. Low Poly v3 (expresiones faciales) — `lowpoly_v3/`
La v2 queda intacta en `lowpoly_v2/`; la v3 la extiende con una cara nueva lista para expresiones.

![Comparación sprite vs v2 vs v3](lowpoly_v3/comparison_v3.png)

- `lillith_lowpoly_v3.blend` / `lillith_lowpoly_v3.glb`: **5.051 triángulos**, mismo rig de 34 huesos.
- Cara nueva low-poly estilo toon: ojos con blanco, iris violeta, pupila, brillo y pestañas; cejas; boca abierta con dientes y lengua.
- **Por defecto sonríe**: la forma base (Basis) ya es una sonrisa alegre.
- **Shape keys** (morph targets en el GLB): `Smile` (sonrisa más amplia), `Happy` (ojos ^^ y risa), `Angry`, `Sad`, `Surprised`, `Blink` y `Wink` (guiño del ojo visible), además de `Wink.L` y `Wink.R`.
- **Idle** ahora incluye parpadeos, y hay una animación nueva **Expressions** que recorre todas las expresiones (7 s). Video: [`expressions_preview.mp4`](lowpoly_v3/expressions_preview.mp4).
- El flequillo está espejado respecto a v2: ahora tapa el ojo izquierdo de Lillith, igual que en el sprite `LM_Suit_V1`, y el ojo visible queda del mismo lado que en el arte.
- Reconstruir: `blender -b -P lowpoly_v3/build_v3.py` (lee `build_v2.py` y lo modifica en memoria; ajusta las rutas `/workspace/lillith-3d` a tu entorno).

![Expresiones](lowpoly_v3/expressions_grid.png)

| Frente | 3/4 |
|---|---|
| ![](lowpoly_v3/render_front_v3.png) | ![](lowpoly_v3/render_34_v3.png) |

**Limitaciones (v3):** la cara son piezas planas apenas sobre la cabeza, así que de perfil extremo parece una calcomanía; el ojo tapado por el flequillo existe pero casi no se ve; `Angry` y `Sad` son sutiles; en el GLB no hay shader toon ni contorno (solo en Blender).

### 7. Low Poly v4 (versión final) — `lowpoly_v4/`
Basada en la v3 (cara con expresiones, flequillo espejado, guiños, rig y animaciones); v2 y v3 quedan intactas.

![Comparación sprite vs v3 vs v4](lowpoly_v4/comparison_v4.png)

- `lillith_lowpoly_v4.blend` / `lillith_lowpoly_v4.glb`: **6.405 triángulos**, mismo rig de 34 huesos y las mismas 9 shape keys de la v3 (sonrisa por defecto, Smile, Happy, Angry, Sad, Surprised, Blink, Wink, Wink.L, Wink.R), con ojos un poco más grandes.
- **Cuerpo**: un poco más de busto y cintura más marcada en el saco, caderas más anchas (falda tubo) y muslos más gruesos, como en el sprite. Traje gris carbón y falda casi negra.
- **Broche de calavera**: ahora va sobre el flequillo, encima del ojo tapado, igual que en el dibujo, y es más grande. Del lado del ojo visible hay dos pasadores plateados.
- **Pelo nuevo**: largo hasta la cintura, con mechones en punta por capas que se abren hacia los lados a la altura de los hombros y los codos, un flequillo grande hacia un lado sobre el ojo tapado, flequillos cortos, volumen arriba entre las orejas y mechones más claros. Está pesado a Head, HairBack.0-2 y SideLock L/R, así que se mueve con las animaciones.
- **Animaciones nuevas**: `Sit` (sentada, bucle de 2 s) y `ChairSpin` (7 s: se acomoda, da dos vueltas en la silla con cara feliz, guiña el ojo al final, y la cola y el pelo se quedan atrás con el giro).
- **Escena de oficina**: `office_chair_spin_v4.blend` y `lillith_office_chairspin_v4.glb` (oficina + Lillith + silla girando juntas en la animación `ChairSpin`). Video: [`chair_spin.mp4`](lowpoly_v4/chair_spin.mp4).
- Los GLB están listos para Sketchfab: la cara es una sola primitiva con paleta de colores (`face_palette_v4*.png`), sin accesores dispersos y con las mallas con skin en la raíz. Pasan el validador de Khronos sin errores ni advertencias.
- Reconstruir: `blender -b -P lowpoly_v4/build_v4.py` y luego `blender -b office/lillith_office.blend -P lowpoly_v4/scene_v4.py -- export` (o `-- render`). Los scripts usan rutas de mi entorno (`/workspace/lillith-3d`, y leen `build_v2.py`); ajústalas antes de usarlos.

![Expresiones v4](lowpoly_v4/expressions_grid.png)

| Frente | 3/4 | Lado |
|---|---|---|
| ![](lowpoly_v4/render_front_v4.png) | ![](lowpoly_v4/render_34_v4.png) | ![](lowpoly_v4/render_side_v4.png) |

**Limitaciones (v4):** el pelo es de mechones rígidos low-poly (sin física; solo sigue los huesos del pelo y la cabeza); sentada, las manos quedan más o menos sobre los apoyabrazos y los pies un poco arriba del piso; la caminata sigue rígida; el saco no tiene solapas ni botones; en los GLB no hay shader toon ni contorno (solo en Blender).

Herramientas: Blender 4.2.3 LTS, Python, `gradio_client`, Pillow y ffmpeg.

## Limitaciones conocidas
- Low-poly v1: cuerpo simplificado (piernas delgadas, manos ovaladas), pelo trasero en un solo bloque, flequillo que se ve flotando de lado, cara muy básica, solo la cola tiene rig y las piezas se superponen en vez de unirse (no apto para impresión 3D).
- TRELLIS: mano levantada deformada, la cara es solo la textura del dibujo y la textura se ve borrosa, sin contornos.

## Licencia
- Modelos, renders y arte: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) © FeithNoir (ver `LICENSE`).
- Código (`lowpoly/build.py`, `run.py`, `render.py`, `bright.py`, `lowpoly_v2/*.py`, `lowpoly_v3/*.py`, `lowpoly_v4/*.py`): MIT.

---
**English:** 3D models of my OC Lillith Murasaki: a scripted low-poly toon model made in Blender (3,487 tris, rigged tail and turntable animation) and an image-to-3D test made with TRELLIS (11,836 tris). Character and art by FeithNoir. Models and art are licensed CC BY-SA 4.0; the scripts are MIT. To rebuild the low-poly model, run `blender -b -P lowpoly/build.py`. **v2** (`lowpoly_v2/`): 4,915 tris, 34-bone Humanoid-style rig, fuller side hair, block-heel pumps, and Idle/Wave/Walk/TailSway animations in the GLB; rebuild with `blender -b -P lowpoly_v2/build_v2.py` (helper scripts reference local `/workspace/lillith-3d` paths).
