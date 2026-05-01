from services.sanitizer import sanitize_input

dirty = "<script>alert('hack')</script> Hello"

clean = sanitize_input(dirty)

print("Cleaned:", clean)