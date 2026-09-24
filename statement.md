# Problem Statement

Manual attendance (register ya excel sheet) mein bahut time lagta hai 
aur galti hone ke chances bhi zyada hote hain. Agar kisi student ka 
attendance % nikalna ho ya kisi din kaun absent tha yeh dekhna ho, to 
manually dhundna padta hai.

Isliye maine ek simple command-line Attendance Marking System banaya 
hai jisme:

- Student ko add kar sakte hain
- Roz ki attendance mark kar sakte hain (Present/Absent)
- Kisi bhi date ka attendance dekh sakte hain
- Student ka attendance % nikal sakte hain
- Sabka overall summary dekh sakte hain

Yeh project sirf terminal se chalta hai, koi GUI nahi hai, aur data 
SQLite database mein save hota hai taaki restart ke baad bhi data 
safe rahe.

## Kaun use kar sakta hai
- Teacher jo apni class ka attendance track karna chahte hain
- Coaching center jahan chhote groups ka attendance manage hota hai