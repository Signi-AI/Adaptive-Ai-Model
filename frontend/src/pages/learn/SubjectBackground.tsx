import { useEffect, useRef, useState } from "react";
import type { Subject } from "./data";

function seeded(seed: number) {
  let s = seed;
  return () => {
    s |= 0;
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function paint(canvas: HTMLCanvasElement, subject: Subject) {
  const parent = canvas.parentElement;
  if (!parent) return;
  const dpr = window.devicePixelRatio || 1;
  const W = parent.clientWidth;
  const H = parent.clientHeight;
  canvas.width = W * dpr;
  canvas.height = H * dpr;
  canvas.style.width = `${W}px`;
  canvas.style.height = `${H}px`;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, W, H);

  const rand = seeded([...subject.key].reduce((a, c) => a * 31 + c.charCodeAt(0), 7));
  const target = W < 600 ? 120 : 165;
  const cols = Math.max(2, Math.round(W / target));
  const rows = Math.max(2, Math.round(H / target));
  const cw = W / cols;
  const ch = H / rows;
  const m = Math.min(cw, ch);

  ctx.fillStyle = subject.color;
  ctx.strokeStyle = subject.color;
  ctx.lineWidth = 2;

  let n = 0;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = (c + 0.5) * cw + (rand() - 0.5) * cw * 0.22;
      const y = (r + 0.5) * ch + (rand() - 0.5) * ch * 0.22;
      const rot = (rand() - 0.5) * 0.6;
      const isShape = (r + c) % 3 === 0;
      const fade = W < 760 ? 1 : Math.min(1, Math.max(0, (Math.abs(x - W / 2) - 300) / 220));

      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(rot);
      ctx.globalAlpha = 0.05 + 0.08 * fade;

      if (!isShape) {
        const g = subject.glyphs[(n++ * 5 + r) % subject.glyphs.length];
        let size = Math.min(34, m * 0.3);
        ctx.font = `600 ${size}px Figtree, sans-serif`;
        const w = ctx.measureText(g).width;
        if (w > cw * 0.62) {
          size = (size * cw * 0.62) / w;
          ctx.font = `600 ${size}px Figtree, sans-serif`;
        }
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(g, 0, 0);
      } else {
        const z = m * 0.28;
        if (subject.shape === "tri") {
          ctx.beginPath();
          ctx.moveTo(0, -z);
          ctx.lineTo(z, z * 0.8);
          ctx.lineTo(-z, z * 0.8);
          ctx.closePath();
          ctx.stroke();
        } else if (subject.shape === "atom") {
          for (let k = 0; k < 3; k++) {
            ctx.rotate(Math.PI / 3);
            ctx.beginPath();
            ctx.ellipse(0, 0, z, z * 0.38, 0, 0, 7);
            ctx.stroke();
          }
          ctx.beginPath();
          ctx.arc(0, 0, 3, 0, 7);
          ctx.fill();
        } else if (subject.shape === "grid") {
          ctx.beginPath();
          ctx.arc(0, 0, z, 0, 7);
          ctx.moveTo(-z, 0);
          ctx.lineTo(z, 0);
          ctx.moveTo(0, -z);
          ctx.lineTo(0, z);
          ctx.stroke();
        } else {
          ctx.beginPath();
          for (let k = -1; k <= 1; k++) {
            ctx.moveTo(-z, k * 9);
            ctx.lineTo(z, k * 9);
          }
          ctx.stroke();
        }
      }
      ctx.restore();
    }
  }
}

export default function SubjectBackground({ subject }: { subject: Subject | null }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setVisible(false);
    const canvas = ref.current;
    if (!subject || !canvas) return;
    const timer = window.setTimeout(() => {
      paint(canvas, subject);
      setVisible(true);
    }, 300);
    const onResize = () => paint(canvas, subject);
    window.addEventListener("resize", onResize);
    return () => {
      window.clearTimeout(timer);
      window.removeEventListener("resize", onResize);
    };
  }, [subject]);

  return (
    <canvas
      ref={ref}
      aria-hidden="true"
      className={`pointer-events-none absolute inset-0 transition-opacity duration-700 motion-reduce:transition-none ${visible ? "opacity-100" : "opacity-0"}`}
    />
  );
}
