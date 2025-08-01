from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
import io

from ats_score import compute_ats_score
from gemini_model import get_llm_response

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        print(f"✅ Received file: {file.filename}")

        contents = await file.read()
        pdf_reader = PdfReader(io.BytesIO(contents))
        resume_text = " ".join(page.extract_text() or "" for page in pdf_reader.pages)

        if not resume_text.strip():
            print("❌ Resume text is empty.")
            return JSONResponse(
                content={"error": "Empty or unreadable resume PDF."},
                status_code=400
            )

        print("✅ Extracted resume text")

        # Gemini prompt
        prompt = f"""
You are an ATS resume expert. The following resume text is from a candidate.

Your job is to:
- Break it into sections (like Education, Experience, etc.)
- Provide a brief section-wise analysis (strengths, issues)
- Give improvement suggestions in bullet points

Only respond in JSON with 3 keys: "sections", "analysis", and "suggestions".

Resume Text:
```txt
{resume_text}
```"""

        try:
            print("⏳ Calling Gemini...")
            llm_json = get_llm_response(prompt)
            print("✅ Gemini response received")

            if not isinstance(llm_json, dict):
                raise ValueError("Gemini did not return a valid JSON object.")

        except Exception as e:
            print("❌ Gemini Error:", str(e))
            return JSONResponse(
                content={"error": "LLM response failed", "details": str(e)},
                status_code=500
            )

        try:
            print("⏳ Computing ATS score...")
            ats_score = compute_ats_score(resume_text, llm_json.get("sections", []))
            print("✅ ATS score computed")
        except Exception as e:
            print("❌ ATS Score Error:", str(e))
            return JSONResponse(
                content={"error": "ATS scoring failed", "details": str(e)},
                status_code=500
            )

        return {
            "llm_analysis": llm_json,
            "ats_score": ats_score
        }

    except Exception as e:
        print("❌ Server Error:", str(e))
        return JSONResponse(
            content={"error": "Unexpected error", "details": str(e)},
            status_code=500
        )
