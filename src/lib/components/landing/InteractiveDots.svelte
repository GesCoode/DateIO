<script lang="ts">
	type Blob = { cx: number; cy: number; rx: number; ry: number; strength?: number };

	const blobs: Blob[] = [
		{ cx: 0.22, cy: 0.2, rx: 0.34, ry: 0.3, strength: 1 },
		{ cx: 0.82, cy: 0.22, rx: 0.2, ry: 0.2, strength: 0.85 },
		{ cx: 0.78, cy: 0.55, rx: 0.28, ry: 0.22, strength: 0.9 },
		{ cx: 0.32, cy: 0.78, rx: 0.3, ry: 0.18, strength: 0.8 }
	];

	const SPACING = 14;
	const REPEL_RADIUS = 150;
	const MAX_PUSH = 24;
	const MAJOR_EVERY = 4;

	let canvas: HTMLCanvasElement | undefined = $state();
	let width = $state(0);
	let height = $state(0);
	let mouse = $state({ x: -9999, y: -9999, active: false });
	let reducedMotion = $state(false);

	let rafId = 0;
	let needsDraw = false;

	function blobIntensity(x: number, y: number, w: number, h: number): number {
		const px = x / w;
		const py = y / h;
		let max = 0;

		for (const b of blobs) {
			const dx = (px - b.cx) / b.rx;
			const dy = (py - b.cy) / b.ry;
			const d = Math.sqrt(dx * dx + dy * dy);
			if (d >= 1) continue;
			const edge = 1 - d;
			const soft = edge * edge * (3 - 2 * edge);
			max = Math.max(max, soft * (b.strength ?? 1));
		}

		return max;
	}

	function repelOffset(x: number, y: number): { ox: number; oy: number } {
		if (!mouse.active || reducedMotion) return { ox: 0, oy: 0 };

		const dx = x - mouse.x;
		const dy = y - mouse.y;
		const dist = Math.hypot(dx, dy);

		if (dist >= REPEL_RADIUS || dist < 0.001) return { ox: 0, oy: 0 };

		const t = 1 - dist / REPEL_RADIUS;
		const force = t * t * MAX_PUSH;
		return {
			ox: (dx / dist) * force,
			oy: (dy / dist) * force
		};
	}

	function draw() {
		needsDraw = false;
		const ctx = canvas?.getContext('2d');
		if (!ctx || width === 0 || height === 0) return;

		ctx.clearRect(0, 0, width, height);

		let row = 0;
		for (let y = SPACING / 2; y < height; y += SPACING, row++) {
			let col = 0;
			for (let x = SPACING / 2; x < width; x += SPACING, col++) {
				const intensity = blobIntensity(x, y, width, height);
				if (intensity < 0.04) continue;

				const { ox, oy } = repelOffset(x, y);
				const isMajor = row % MAJOR_EVERY === 0 && col % MAJOR_EVERY === 0;
				const alpha = intensity * (isMajor ? 0.55 : 0.32);
				const radius = isMajor ? 1.35 : 0.85;

				ctx.beginPath();
				ctx.arc(x + ox, y + oy, radius, 0, Math.PI * 2);
				ctx.fillStyle = isMajor
					? `rgba(200, 184, 154, ${alpha * 0.9})`
					: `rgba(126, 205, 184, ${alpha * 0.75})`;
				ctx.fill();
			}
		}
	}

	function scheduleDraw() {
		if (needsDraw) return;
		needsDraw = true;
		rafId = requestAnimationFrame(draw);
	}

	function resize() {
		if (!canvas) return;
		const dpr = Math.min(window.devicePixelRatio ?? 1, 2);
		width = window.innerWidth;
		height = window.innerHeight;
		canvas.width = Math.floor(width * dpr);
		canvas.height = Math.floor(height * dpr);
		canvas.style.width = `${width}px`;
		canvas.style.height = `${height}px`;
		const ctx = canvas.getContext('2d');
		ctx?.setTransform(dpr, 0, 0, dpr, 0, 0);
		draw();
	}

	function onPointerMove(event: PointerEvent) {
		mouse = { x: event.clientX, y: event.clientY, active: true };
		scheduleDraw();
	}

	function onPointerLeave() {
		mouse = { x: -9999, y: -9999, active: false };
		scheduleDraw();
	}

	$effect(() => {
		reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		resize();

		const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
		const onMq = () => {
			reducedMotion = mq.matches;
			draw();
		};
		mq.addEventListener('change', onMq);
		window.addEventListener('resize', resize);
		window.addEventListener('pointermove', onPointerMove, { passive: true });
		document.documentElement.addEventListener('pointerleave', onPointerLeave);

		return () => {
			mq.removeEventListener('change', onMq);
			window.removeEventListener('resize', resize);
			window.removeEventListener('pointermove', onPointerMove);
			document.documentElement.removeEventListener('pointerleave', onPointerLeave);
			cancelAnimationFrame(rafId);
		};
	});
</script>

<canvas bind:this={canvas} class="interactive-dots" aria-hidden="true"></canvas>

<style>
	.interactive-dots {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
	}
</style>
