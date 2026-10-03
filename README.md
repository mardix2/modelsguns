# modelsguns — модели оружия для мода на Fabric (GeckoLib)

Детализированные 3D-модели оружия для Minecraft **26.2 + Fabric + GeckoLib 5**:
геометрия Bedrock (`.geo.json`) с костями под анимации, анимации, текстуры и
определения предметов. Плюс проекты Blockbench для ручной доработки.

![Все стволы](previews/all_guns.png)

| Ствол | id | Кубов | Подвижные кости | Анимации |
|---|---|---|---|---|
| MK18 Mod 1 | `mk18` | 511 | bolt, charging_handle, trigger, dust_cover, magazine | shoot, reload |
| Glock 17 Gen 5 | `glock17` | 209 | slide, barrel, trigger, magazine | shoot, reload |
| AK-47 Type 3 | `ak47` | 555 | bolt, trigger, selector, top_cover, magazine | shoot, reload |
| Desert Eagle .50 AE | `deagle` | 276 | slide, hammer, trigger, magazine | shoot, reload |
| H&K MP5A5 | `mp5a5` | 549 | cocking_handle, trigger, magazine | shoot, reload |
| Remington 870 Wingmaster | `m870` | 276 | pump, trigger, shell | shoot, pump, reload |
| AI AWM .338 | `awm` | 406 | bolt, trigger, magazine | shoot, bolt, reload |

Только само оружие: без прицелов, фонарей и прочего обвеса (у AWM — только
планка под оптику). Пропорции взяты из реальных размеров (длина, ствол, высота).

## Что внутри

```
geckolib/assets/modelsguns/             -> скопировать в src/main/resources/assets/<modid>/
  geckolib/models/item/<id>.geo.json       геометрия (Bedrock 1.12.0), кости = группы
  geckolib/animations/item/<id>.animation.json
  textures/item/<id>.png
  models/item/<id>.json                    базовая модель: положение в руке / GUI / рамке
  items/<id>.json                          minecraft:special -> geckolib:geckolib
geckolib/example/                       пример кода (Fabric 26.2, Mojang-имена, GeckoLib 5)
blockbench/<id>.bbmodel                 проекты Blockbench (формат Bedrock Model, текстура встроена)
previews/                               рендеры с разных сторон
tools/                                  генератор моделей на Python
```

## Подключение к моду

1. Подключите GeckoLib 5 для 26.2 (Fabric) как зависимость мода.
2. Скопируйте `geckolib/assets/modelsguns/*` в `src/main/resources/assets/<ваш_modid>/`.
   Файлы не ссылаются на namespace, кроме `items/*.json` и `models/item/*.json`
   (там `modelsguns:item/<id>`) — замените `modelsguns` на свой modid.
3. Зарегистрируйте предметы, как в `geckolib/example/`:
   - `GunItem` реализует `GeoItem`;
   - в `createGeoRenderer` отдаёт `GeoItemRenderer` с `DefaultedItemGeoModel`,
     который сам найдёт `geckolib/models/item/<id>.geo.json`,
     `geckolib/animations/item/<id>.animation.json` и `textures/item/<id>.png`;
   - предмет регистрируется с `Item.Properties().setId(key)`.
4. Анимации запускаются по имени `animation.<id>.<имя>`, например
   `triggerAnim(player, GeoItem.getOrAssignId(stack, serverLevel), "main", "shoot")`.

Пути, формат UV, порядок поворотов и знаки анимаций сверены с исходниками
GeckoLib (ветка `26.2`). В игре модели и пример кода не запускались — это шаблон.

## Стиль и технические детали

- Наклонные детали (рукояти, приклады, изогнутые магазины, спуски) строятся в
  повёрнутых «системах координат», поэтому у них настоящие фаски под 45°, а
  изгибы магазинов плавные (цепочка сегментов с шагом 1.5–2.5°).
- Фаски на длинных рёбрах с бликами, восьмигранные «цилиндры», ровная
  «нарисованная» текстура: шлифованная сталь, дерево, клетчатый стиплинг,
  насечка на дереве, маркировка.
- Полностью скрытые внутри грани не текстурируются; у подвижных деталей грани
  оставлены, чтобы их было видно во время анимации.
- Из-за поворотов по нескольким осям модели больше не подходят для ванильных
  Java-моделей предметов — только GeckoLib/Bedrock.

## Пересборка / новые стволы

```
pip install pillow numpy
python3 tools/build.py          # все стволы
python3 tools/build.py ak47     # только один
```

Каждый ствол — файл `tools/<id>.py` с функцией `build()`, `GRIP_POINT`, `DISPLAY`
и `ANIMATIONS` (ключевые кадры в пространстве модели), плюс строка в
`GUN_MODULES` в `tools/build.py`. Деталь — одна строка
`B("имя", x0, y0, z0, x1, y1, z1, материал, кость, узор)`; для скруглённых деталей
есть `bevel`, `cyl_z`, `cyl_x`, `ring_z`, `pin_x`, `teeth_z`, `rail_z`, а для
наклонных частей — `with m.frame(("x", угол, точка)):` и `m.chain(...)`.
