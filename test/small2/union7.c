#include "../small1/testharness.h"

// NUMERRORS 12

enum tags {
  TAG_ZERO = 0,
};

struct host {
  int tag; // 0 for integer, 1 for pointer to int, 2 for structure 
  union bar {
    int anint     __SELECTEDWHEN("tag" == TAG_ZERO);
    int * ptrint  __SELECTEDWHEN("tag" == 1);
    struct str {
      int * * ptrptr;
    } ptrptr    
        __SELECTEDWHEN("tag" == 5) // ERROR(0)
         /* missing selected when */ // ERROR(1):Error 1
        __SELECTEDWHEN("tag" == foo) // ERROR(2):Cannot compile the discriminator
        __SELECTEDWHEN("tag_bad" == 5) // ERROR(3):Cannot compile the discriminator
         __SELECTEDWHEN("tag" == 5) __SELECTEDWHEN("tag" == 6) // ERROR(4):more than one SELECTEDWHEN clause
#if ERROR >= 5
        __SELECTEDWHEN("tag" == 5)
#endif         
         ;
  } data;
  int * somethingelse;      
} g;
  

int x;
int * px = &x;

int main() {

  g.tag = 0;

  // This is good behavior
  
#if ERROR == 0 
  g.data.anint = 5;
  x = g.data.anint;

  
  g.tag = 1;
  g.data.ptrint = px;
  px = g.data.ptrint;

  g.tag = 5;
  g.data.ptrptr.ptrptr = &px;
  x = * * g.data.ptrptr.ptrptr;

  // This is allowed because we are not reading a poinetr
  g.tag = 1; x = g.data.anint;

#endif

  if(KIND_OF(g.data.ptrint) != SAFE_KIND) E(1);// ERROR(1)

  
  // We cannot access pointers when the tag is wrong
  g.tag = 0; x = g.data.ptrint; // ERROR(5):Failure WRONGFIELD
  g.tag = 0; * g.data.ptrptr.ptrptr = x; // ERROR(6):Failure WRONGFIELD
  g.tag = 0; { struct str s = g.data.ptrptr; } // ERROR(7):Failure WRONGFIELD
  
#if ERROR == 8
  {
    union {
      int * ptr  __SELECTEDWHEN("tag");
    } a;
     // We should not be able to acces this one
    // ERROR(8):outside a host structure
    px = a.ptr;
  }
#endif    

  // We cannot take the address of fields in discriminated unions
  px = & g.data.anint; // ERROR(9):cannot take the address of a field
  // We cannot take the address of a field in a subfield
  { int * * * a = & g.data.ptrptr.ptrptr; } // ERROR(10):cannot take the address of a field

  // We can take the address of a non-discriminated field
  px = & g.somethingelse; E(11); // ERROR(11):Error 11

  // When we switch tags we clear the pointers
  g.tag = 1; g.data.ptrint = &x; g.tag = 0; if(! g.data.anint) E(12); // ERROR(12):Error 12
  
  SUCCESS;
}
