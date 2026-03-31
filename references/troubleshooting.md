# Known Issues & Fixes

## Motion Canvas Rendering

### Issue: headless: 'new' produces blank canvas
Motion Canvas animations render to HTML5 Canvas, which doesn't work in headless Chrome.
**Fix:** Always use `headless: false` in Puppeteer.

### Issue: ffmpeg "No such file or directory" for audio
Motion Canvas's ffmpeg plugin passes audio paths directly to ffmpeg subprocess.
If the path is relative or Vite-relative, ffmpeg can't find it.
**Fix:** Disable audio in project.ts, merge audio separately with ffmpeg after rendering.

### Issue: UI covers the animation canvas
Motion Canvas loads its editor UI by default. The actual animation renders behind it.
**Fix:** The Vite plugin + ffmpeg handles rendering correctly via the Render button.
Don't try to screenshot the page directly—the output goes to `output/` directory.

### Issue: Vite FS allow list blocks node_modules
```
The request url ".../node_modules/..." is outside of Vite serving allow list.
```
**Fix:** Set `server.fs.allow` to include the project root and `/tmp`.

### Issue: `@motion-canvas/cli` package not found
There is no standalone CLI package. Rendering requires the vite-plugin pipeline.
**Fix:** Use Puppeteer to launch Chrome, navigate to dev server, click Render button.

## Chrome Requirements

macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
Linux: `/usr/bin/google-chrome`

Chrome must be installed (Chromium alone may not work due to codec support).

## Output Location

Rendered video goes to `<project>/output/<project-name>.mp4`.
This is the Motion Canvas default, not configurable via project.ts.
