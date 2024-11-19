#!/bin/bash

INPUT_DIR="inputs"
OUTPUT_COMPRESSED_DIR="outputs/compressed"
OUTPUT_DECOMPRESSED_DIR="outputs/decompressed"

MINBITS=10
MAXBITS=15  

for CATEGORY in binario; do
  CATEGORY_INPUT_DIR="$INPUT_DIR/$CATEGORY"
  CATEGORY_COMPRESSED_DIR="$OUTPUT_COMPRESSED_DIR/$CATEGORY"
  CATEGORY_DECOMPRESSED_DIR="$OUTPUT_DECOMPRESSED_DIR/$CATEGORY"
    
  mkdir -p "$CATEGORY_COMPRESSED_DIR" "$CATEGORY_DECOMPRESSED_DIR"

  for FILE in "$CATEGORY_INPUT_DIR"/*; do
    if [[ -f "$FILE" ]]; then
      BASENAME=$(basename -- "$FILE")
      FILENAME="${BASENAME%.*}"

      for ((CURBITS = $MINBITS; CURBITS <= $MAXBITS; CURBITS++)); do
        for VARIANT in variable fixed; do

          COMPRESSED_FILE="$CATEGORY_COMPRESSED_DIR/$FILENAME-$CURBITS-$VARIANT.lzw"
          
          # get extension
          EXTENSION="${FILE##*.}"

          DECOMPRESSED_FILE="$CATEGORY_DECOMPRESSED_DIR/$FILENAME-$CURBITS-$VARIANT.$EXTENSION"
          # Run the compression command
          echo "Compressing $FILE -> $COMPRESSED_FILE with maxbits=$CURBITS and variant=$VARIANT"
          python3 main.py --mode compress --stats "$FILE" "$COMPRESSED_FILE" --maxbits "$CURBITS" --variant "$VARIANT"

          # Run the decompression command
          echo "Decompressing $COMPRESSED_FILE -> $DECOMPRESSED_FILE with maxbits=$CURBITS and variant=$VARIANT"
          python3 main.py --mode decompress --stats "$COMPRESSED_FILE" "$DECOMPRESSED_FILE" --maxbits "$CURBITS" --variant "$VARIANT"
        done
      done
    fi
  done
done
