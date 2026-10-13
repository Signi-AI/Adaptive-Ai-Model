import { useEffect, useRef, useState } from "react";
import type { ReactNode } from "react";
import {
  Check,
  Copy,
  RefreshCw,
  Sparkles,
  Square,
  Volume2,
} from "lucide-react";

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

export default function AiMessage({
  paragraphs,
  showActions,
  onStart,
  onDone,
  onTick,
  children,
}: Props) {
  const total = paragraphs.reduce((sum, p) => sum + p.length, 0);

  const [shown, setShown] = useState(0);
  const [run, setRun] = useState(0);
  const [speaking, setSpeaking] = useState(false);
  const [copied, setCopied] = useState(false);

  const done = shown >= total;

  const startRef = useRef(onStart);
  const doneRef = useRef(onDone);
  const tickRef = useRef(onTick);

  const doneCalledRef = useRef(false);
  const copyTimeoutRef = useRef<number | null>(null);

  startRef.current = onStart;
  doneRef.current = onDone;
  tickRef.current = onTick;

  /*
   * Reset completion state whenever this message
   * starts/restarts or its content changes.
   */
  useEffect(() => {
    doneCalledRef.current = false;
  }, [run, total]);

  /*
   * Typing animation
   */
  useEffect(() => {
    startRef.current?.();

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setShown(total);
      return;
    }

    if (total === 0) {
      setShown(0);
      return;
    }

    const id = window.setInterval(() => {
      setShown((s) => {
        if (s >= total) {
          window.clearInterval(id);
          return s;
        }

        return Math.min(s + 3, total);
      });
    }, 16);

    return () => {
      window.clearInterval(id);
    };
  }, [run, total]);

  /*
   * Tick + done callbacks
   */
  useEffect(() => {
    tickRef.current?.();

    if (done && !doneCalledRef.current) {
      doneCalledRef.current = true;
      doneRef.current?.();
    }
  }, [shown, done]);

  /*
   * Cancel speech when component is removed.
   */
  useEffect(() => {
    return () => {
      window.speechSynthesis?.cancel();

      if (copyTimeoutRef.current !== null) {
        window.clearTimeout(copyTimeoutRef.current);
      }
    };
  }, []);

  /*
   * Stop speech if the message content changes.
   */
  useEffect(() => {
    window.speechSynthesis?.cancel();
    setSpeaking(false);
  }, [paragraphs]);

  const plain = paragraphs.join(" ");

  /*
   * Read aloud / stop reading
   */
  const speak = () => {
    const synth = window.speechSynthesis;

    if (!synth || !plain.trim()) {
      return;
    }

    if (speaking) {
      synth.cancel();
      setSpeaking(false);
      return;
    }

    synth.cancel();

    const u = new SpeechSynthesisUtterance(plain);

    u.rate = 0.95;

    u.onend = () => {
      setSpeaking(false);
    };

    u.onerror = () => {
      setSpeaking(false);
    };

    setSpeaking(true);
    synth.speak(u);
  };

  /*
   * Copy message
   */
  const copy = async () => {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(plain);
      } else {
        throw new Error("Clipboard API unavailable");
      }
    } catch {
      const area = document.createElement("textarea");

      area.value = plain;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      area.style.pointerEvents = "none";

      document.body.appendChild(area);

      area.focus();
      area.select();

      try {
        document.execCommand("copy");
      } catch {
        // Ignore copy failure.
      }

      document.body.removeChild(area);
    }

    setCopied(true);

    if (copyTimeoutRef.current !== null) {
      window.clearTimeout(copyTimeoutRef.current);
    }

    copyTimeoutRef.current = window.setTimeout(() => {
      setCopied(false);
      copyTimeoutRef.current = null;
    }, 1500);
  };

  /*
   * Retry typing animation
   */
  const retry = () => {
    window.speechSynthesis?.cancel();

    setSpeaking(false);
    setCopied(false);

    doneCalledRef.current = false;

    setShown(0);
    setRun((r) => r + 1);
  };

  /*
   * Calculate which characters should currently be visible.
   */
  let left = shown;

  const parts = paragraphs.map((p) => {
    const part = left > 0 ? p.slice(0, left) : "";

    left -= p.length;

    return part;
  });

  const last = parts.reduce(
    (idx, part, i) => (part ? i : idx),
    -1,
  );

  return (
    <div className="my-6 min-w-0">
      <div className="mb-1.5 grid h-6 w-6 place-items-center rounded-full bg-learn-accent text-white transition-colors duration-500">
        <Sparkles size={13} />
      </div>

      <div>
        {parts.map((part, i) =>
          part ? (
            <p
              key={i}
              className={`mb-3 last:mb-0 ${
                !done && i === last ? "learn-cursor" : ""
              }`}
            >
              {part}
            </p>
          ) : null,
        )}
      </div>

      {done && showActions && (
        <div className="-ml-2 mt-2 flex gap-0.5">
          <button
            type="button"
            className={`${iconBtn} ${
              speaking ? "text-learn-accent" : ""
            }`}
            onClick={speak}
            aria-label={
              speaking ? "Stop reading" : "Read aloud"
            }
            title={speaking ? "Stop" : "Read aloud"}
          >
            {speaking ? (
              <Square size={17} />
            ) : (
              <Volume2 size={18} />
            )}
          </button>

          <button
            type="button"
            className={`${iconBtn} ${
              copied ? "text-learn-accent" : ""
            }`}
            onClick={copy}
            aria-label="Copy"
            title="Copy"
          >
            {copied ? (
              <Check size={18} />
            ) : (
              <Copy size={18} />
            )}
          </button>

          <button
            type="button"
            className={iconBtn}
            onClick={retry}
            aria-label="Try again"
            title="Try again"
          >
            <RefreshCw size={18} />
          </button>
        </div>
      )}

      {done && children}
    </div>
  );
}