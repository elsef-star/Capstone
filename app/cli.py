import sys
from app.services.vision import analyze_image_with_vision
from app.services.guard import evaluate_mismatch_guard

def main():
    if len(sys.argv) < 2:
        print("İstifadə əmri: python -m app.cli <şəkil_faylı>")
        return

    file_path = sys.argv[1]
    
    try:
        with open(file_path, "rb") as f:
            image_bytes = f.read()
        
        print(f"\n[GEMINI VISION] '{file_path}' şəkli skan olunur...")
        metadata, cost = analyze_image_with_vision(image_bytes)
        
        print("\n================ TƏHLİL NƏTİCƏSİ ================")
        print(f" Aşkarlanan Subyekt : {metadata.subject.upper()}")
        print(f" Kateqoriya          : {metadata.category}")
        print(f" Dəqiqlik (Score)    : %{metadata.confidence * 100:.1f}")
        print(f" Xüsusiyyətlər       : {', '.join(metadata.attributes)}")
        print(f" Təsvir              : {metadata.caption}")
        print("==================================================")

        # Məqalə ilə uyğunluq testi (Red Fox Article)
        target_post_title = "The Habitat and Behavior of Red Foxes"
        is_safe, reason = evaluate_mismatch_guard(
            post_title=target_post_title,
            image_subject=metadata.subject,
            image_category=metadata.category,
            confidence=metadata.confidence,
            similarity_score=0.88
        )

        print("\n MƏQALƏ İLƏ UYĞUNLUQ STRUKTURU:")
        print(f" Məqalə Adı : '{target_post_title}'")
        if is_safe:
            print(f" Status     : [APPROVED / UYĞUNDUR] -> {reason}")
        else:
            print(f" Status     : [REJECTED / UYĞUN DEYİL] -> {reason}")
        print("==================================================\n")

    except Exception as e:
        print(f"\n[XƏTA BANERİ]: {e}")
        print("Lütfən .env faylındakı GEMINI_API_KEY dəyərini yoxlayın.\n")

if __name__ == "__main__":
    main()