import { useEffect, useRef, useState } from "react";
import type { ReactNode } from "react";
import { Check, Copy, RefreshCw, Sparkles, Square, Volume2 } from "lucide-react";

interface Props {
  paragraphs: string[];
  showActions?: boolean;
  onStart?: () => void;
  onDone?: () => void;
  onTick?: () => void;
  children?: ReactNode;
}

const iconBtn =
  "grid h-8 w-8 place-items-center rounded-lg text-learn-muted transition-colors hover:bg-learn-hover hover:text-learn-ink focus-visible:outline focus-visible:outline-2 focus-visible:outline-learn-accent";

export default function AiMessage({ paragraphs, showActions, onStart, onDone, onTick, children }: Props) {
  const total = paragraphs.reduce((sum, p) => sum + p.length, 0);
  const [shown, setShown] = useState(0);
  const [run, setRun] = useState(0);
  const [speaking, setSpeaking] = useState(false);
  const [copied, setCopied] = useState(false);
  const done = shown >= total;

  const startRef = useRef(onStart);
  const doneRef = useRef(onDone);
  const tickRef = useRef(onTick);
  startRef.current = onStart;
  doneRef.current = onDone;
  tickRef.current = onTick;

  useEffect(() => {
    startRef.current?.();
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setShown(total);
      return;
    }
    const id = window.setInterval(() => {
      setShown((s) => {
        if (s >= total) {
          window.clearInterval(id);
          return s;
        }
        return s + 3;
      });
    }, 16);
    return () => window.clearInterval(id);
  }, [run, total]);

  useEffect(() => {
    tickRef.current?.();
    if (done) doneRef.current?.();
  }, [shown, done]);

  useEffect(() => () => window.speechSynthesis?.cancel(), []);

  const plain = paragraphs.join(" ");

  const speak = () => {
    const synth = window.speechSynthesis;
    if (!synth) return;
    if (speaking) {
      synth.cancel();
      setSpeaking(false);
      return;
    }
    synth.cancel();
    const u = new SpeechSynthesisUtterance(plain);
    u.rate = 0.95;
    u.onend = () => setSpeaking(false);
    u.onerror = () => setSpeaking(false);
    setSpeaking(true);
    synth.speak(u);
  };

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(plain);
    } catch {
      const area = document.createElement("textarea");
      area.value = plain;
      document.body.appendChild(area);
      area.select();
      document.execCommand("copy");
      area.remove();
    }
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1500);
  };

  const retry = () => {
    window.speechSynthesis?.cancel();
    setSpeaking(false);
    setShown(0);
    setRun((r) => r + 1);
  };

  let left = shown;
  const parts = paragraphs.map((p) => {
    const part = left > 0 ? p.slice(0, left) : "";
    left -= p.length;
    return part;
  });
  const last = parts.reduce((idx, part, i) => (part ? i : idx), -1);

  return (
    <div className="my-6 min-w-0">
      <div className="mb-1.5 grid h-6 w-6 place-items-center rounded-full bg-learn-accent text-white transition-colors duration-500">
        <Sparkles size={13} />
      </div>
      <div>
        {parts.map((part, i) =>
          part ? (
            <p key={i} className={`mb-3 last:mb-0 ${!done && i === last ? "learn-cursor" : ""}`}>
              {part}
            </p>
          ) : null,
        )}
      </div>
      {done && showActions && (
        <div className="-ml-2 mt-2 flex gap-0.5">
          <button type="button" className={`${iconBtn} ${speaking ? "text-learn-accent" : ""}`} onClick={speak} aria-label={speaking ? "Stop reading" : "Read aloud"} title={speaking ? "Stop" : "Read aloud"}>
            {speaking ? <Square size={17} /> : <Volume2 size={18} />}
          </button>
          <button type="button" className={`${iconBtn} ${copied ? "text-learn-accent" : ""}`} onClick={copy} aria-label="Copy" title="Copy">
            {copied ? <Check size={18} /> : <Copy size={18} />}
          </button>
          <button type="button" className={iconBtn} onClick={retry} aria-label="Try again" title="Try again">
            <RefreshCw size={18} />
          </button>
        </div>
      )}
      {done && children}
    </div>
  );
}
