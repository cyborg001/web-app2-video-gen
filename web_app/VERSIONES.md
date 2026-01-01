# Registro de Versiones - Video Generator Web App (web_app2)

Este archivo registra la evolución técnica, nuevas funcionalidades y correcciones de la aplicación.

| Versión | Fecha | Hito Técnico | Cambios Realizados |
| :--- | :--- | :--- | :--- |
| 2.0.0 | 2025-12-27 | Lanzamiento Dist | Creación de la versión independiente (dist) con sistema de migraciones automáticas. |
| 2.1.0 | 2025-12-28 | IA Scripting | Integración de Gemini Pro para generación automática de guiones y prompts visuales. |
| 2.2.0 | 2026-01-01 | **Professional Finish Update** | **Ken Burns Granular:** Control de dirección desde el guion. <br> **Audio Ducking:** Atenuación automática de música. <br> **Visual Asset:** Video CTA animado integrado. |
| 2.2.1 | 2026-01-01 | **Audio Ducking Hotfix** | Solución a error `unsupported operand type`. |
| 2.2.2 | 2026-01-01 | **Numpy Vectorization Fix** | Soporte para procesamiento de arreglos en Ducking. |
| 2.2.3 | 2026-01-01 | **Title Integrity Shield** | Blindaje del modelo para evitar sobrescritura de títulos. |
| 2.2.5 | 2026-01-01 | **Audio Stereo Fix** | Soporte para broadcasting en audio estéreo (2 canales). |
| 2.3.0 | 2026-01-01 | **Silent Breaks & UX** | Soporte para etiqueta `[PAUSA:segundos]` en el guion. |
| 2.4.0 | 2026-01-01 | **Professional Finish & Fades** | **Audio Fades:** Suavizado de 0.2s en transiciones (sin ruidos). <br> **UI Guide:** Ejemplos maestros de DIR y PAUSA en la interfaz. |
| 2.5.0 | 2026-01-01 | **UI Simplification** | Eliminación del checkbox redundante "Activar Desplazamiento Dinámico". Ahora el efecto Ken Burns se activa exclusivamente mediante el guion (`DIR`). |
| 2.6.0 | 2026-01-01 | **Strategic Scripting** | Aplicación de la **Ley del Gancho** y **Conclusión Profunda** en guiones. Integración de pausas rítmicas para maximizar el Audio Ducking. |
| 2.8.0 | 2026-01-01 | **Advanced Ken Burns** | Control quirúrgico del encuadre mediante porcentajes (`DIR:START:END`). Permite sub-movimientos precisos en cualquier dirección. |
| 2.9.0 | 2026-01-01 | **Pro Standalone Sync** | Independización total del repositorio, nuevo README profesional y descripción de alto nivel para GitHub. |
| 2.9.4 | 2026-01-01 | **AI Scripting Pro** | Actualización del cerebro IA (Gemini) para generar guiones en formato de 4 columnas, con control de Ken Burns y pausas rítmicas automáticas. |
| 2.9.5 | 2026-01-01 | **Pause Hotfix** | Corrección de error crítico en `AudioClip` para compatibilidad con MoviePy 2.0. |
| 2.9.6 | 2026-01-01 | **Steady Render & Robust Parser** | Generación de silencios en memoria (Stereo) para evitar OSErrors. Limpieza inteligente de nombres de archivo y soporte total para Ken Burns avanzado en el parser. |
| 2.9.8 | 2026-01-01 | **Human-Centric Gemini Fix** | Migración al endpoint estable `v1` y modelo `gemini-1.5-flash-latest`. Implementación de mensajes de error "humanizados" para una mejor experiencia de usuario. |

---
*Actualizado al 01-01-2026*
