export type Shape = "tri" | "atom" | "line" | "grid";

export interface TopicGroup {
  title: string;
  lessons: string[];
}

export interface Subject {
  key: string;
  name: string;
  icon: string;
  color: string;
  glyphs: string[];
  shape: Shape;
  topics: TopicGroup[];
}

export const LEVELS = ["Form 1", "Form 2", "Form 3", "Form 4"];

export const SUBJECTS: Subject[] = [
  {
    key: "math",
    name: "Mathematics",
    icon: "∑",
    color: "#8b5cf6",
    glyphs: ["π", "∑", "√", "x²", "∠", "△", "∫", "%", "÷", "a²+b²=c²", "sin θ", "y=mx+c", "∞", "≠"],
    shape: "tri",
    topics: [
      { title: "Algebra", lessons: ["Expressions", "Linear equations", "Factorising"] },
      { title: "Geometry", lessons: ["Angles", "Triangles", "Circles"] },
      { title: "Statistics", lessons: ["Mean and median", "Reading graphs"] },
    ],
  },
  {
    key: "sci",
    name: "Science",
    icon: "⚛",
    color: "#10b981",
    glyphs: ["H₂O", "⚛", "E=mc²", "DNA", "CO₂", "O₂", "NaCl", "pH", "Fe", "F=ma", "Δ"],
    shape: "atom",
    topics: [
      { title: "Matter", lessons: ["States of matter", "Atoms and elements"] },
      { title: "Energy", lessons: ["Forms of energy", "Heat transfer"] },
      { title: "Living things", lessons: ["Cells", "Photosynthesis"] },
    ],
  },
  {
    key: "eng",
    name: "English",
    icon: "Aa",
    color: "#f59e0b",
    glyphs: ["A", "b", "Q", "“…”", "noun", "verb", "?", "!", "story", "grammar", "Aa"],
    shape: "line",
    topics: [
      { title: "Grammar", lessons: ["Nouns and verbs", "Tenses", "Punctuation"] },
      { title: "Writing", lessons: ["Paragraphs", "Letter writing"] },
      { title: "Reading", lessons: ["Finding the main idea"] },
    ],
  },
  {
    key: "swa",
    name: "Kiswahili",
    icon: "Kk",
    color: "#ef4444",
    glyphs: ["A", "E", "I", "O", "U", "methali", "sarufi", "mwalimu", "ngoma", "jambo", "kitabu"],
    shape: "line",
    topics: [
      { title: "Sarufi", lessons: ["Nomino", "Vitenzi"] },
      { title: "Insha", lessons: ["Barua", "Hadithi fupi"] },
      { title: "Methali", lessons: ["Maana ya methali"] },
    ],
  },
  {
    key: "his",
    name: "History",
    icon: "⏳",
    color: "#b45309",
    glyphs: ["1961", "1884", "⚔", "Kilwa", "Zanzibar", "scroll", "map", "Ujamaa", "1964"],
    shape: "line",
    topics: [
      { title: "Early societies", lessons: ["Stone Age", "Iron Age"] },
      { title: "Colonial period", lessons: ["Berlin Conference", "Resistance"] },
      { title: "Independence", lessons: ["TANU", "1961"] },
    ],
  },
  {
    key: "geo",
    name: "Geography",
    icon: "◍",
    color: "#0ea5e9",
    glyphs: ["N", "S", "E", "W", "Equator", "°C", "mm", "delta", "lat", "long", "scale"],
    shape: "grid",
    topics: [
      { title: "Maps", lessons: ["Scale", "Grid references"] },
      { title: "Weather", lessons: ["Rainfall", "Temperature"] },
      { title: "Landforms", lessons: ["Mountains", "Rivers"] },
    ],
  },
];

const LESSONS: Record<string, string[]> = {
  Expressions: [
    "An algebraic expression is a mix of numbers and letters, like 3x + 5. The letter x stands for a number we do not know yet.",
    "Think of x as an empty box. In 3x + 5, you take three of those boxes and add 5 more.",
    "If x = 2, then 3x + 5 = 3 × 2 + 5 = 11. Replacing the letter with a number is called substitution.",
  ],
  "Linear equations": [
    "An equation says two sides are equal, like 2x + 3 = 11. Our job is to find the x that keeps both sides balanced.",
    "Treat it like a balance scale. Whatever you do to one side, you must do to the other. Subtract 3 from both sides: 2x = 8.",
    "Now divide both sides by 2: x = 4. Check it: 2 × 4 + 3 = 11. It balances, so the answer is right.",
  ],
  Angles: [
    "An angle is the amount of turn between two lines that meet at a point. We measure it in degrees.",
    "A right angle is 90°, like the corner of your book. A straight line is 180°. A full turn is 360°.",
    "Angles on a straight line add up to 180°. If one angle is 120°, the other must be 60°.",
  ],
  Triangles: [
    "A triangle has three sides and three angles. The three angles always add up to 180°.",
    "If two angles are 50° and 60°, the third is 180 − 50 − 60 = 70°.",
    "In a right-angled triangle, a² + b² = c². The longest side, c, is opposite the right angle.",
  ],
};

export function lessonText(subject: Subject, topic: string, lesson: string, level: string): string[] {
  const known = LESSONS[lesson];
  const body = known ?? [
    `The big idea of ${lesson} is the foundation for the next lessons in ${topic}. First I give you the idea in one sentence, then an example, then you try one yourself.`,
    `This is a demo lesson. When the AI engine is connected, this text will be written for ${subject.name}, ${level}, in simple language.`,
  ];
  return [`Let's start with ${lesson}.`, ...body];
}
