# Architecture Documentation

## Guiding principle

The Adaptive Learning Engine must remain independent of:
- any UI technology
- the concrete database implementation
- any specific AI / LLM provider

This allows the same core to be reused from CLI, mobile, web, PWA or a local school server.

## Layers

1. **Domain** (`app/domain`)  
   Pure dataclasses: Student, Topic, Question, Mastery, AnswerAttempt, etc.  
   No I/O.

2. **Repositories** (`app/repositories`)  
   Abstract interfaces + SQLite implementations.  
   Domain and engines depend only on the interfaces.

3. **Adaptive Engine** (`app/adaptive_engine`)  
   MasteryCalculator, DifficultySelector, KnowledgeDiagnoser,  
   RecommendationEngine, LearningPathGenerator, MistakeAnalyzer, QuestionSelector.  
   All deterministic and offline.

4. **Content Engine** (`app/content_engine`)  
   Lessons, questions, answer validation, topic helpers.

5. **Feedback Engine** (`app/feedback`)  
   Instant feedback; optionally enriched by AIProvider.

6. **AI Layer** (`app/ai`) – optional  
   `AIProvider` interface + Null + Mock. Future: llama.cpp / Ollama / TFLite.

7. **Application Service** (`app/services`)  
   `AdaptiveLearningService` – the single façade clients should call.

8. **Database** (`app/database`)  
   SQLAlchemy models and session factory. Only repositories talk to it.

## Data flow – submit_answer

1. Client → `service.submit_answer(...)`
2. Load Question + Student
3. ContentEngine validates answer → AnswerResult
4. Persist AnswerAttempt
5. MistakeAnalyzer updates consecutive / total mistakes
6. MasteryCalculator updates score (0–100)
7. Persist Mastery
8. FeedbackEngine builds message (optional AI enrichment)
9. Return structured result to client

## Why SQLite

- Zero configuration, single file
- Works completely offline
- Sufficient performance for on-device student profiles
- Easy future sync (copy or delta the file)

## Future extension points

- Sync adapter (optional) that pushes/pulls the SQLite file or a change log
- Alternative repository backends (in-memory for tests, or another embedded DB)
- Richer answer validators (numeric tolerance, synonyms)
- Full spaced-repetition scheduler behind the existing interface
- Local LLM implementations of AIProvider
