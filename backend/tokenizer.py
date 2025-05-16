import os
import tempfile
import sentencepiece as spm
import logging
import numpy as np

logger = logging.getLogger(__name__)

class TextTokenizer:
    """SentencePiece-based tokenizer optimized for medical text"""
    def __init__(self, vocab_size=20000, model_type="bpe", max_sequence_length=512):
        self.vocab_size = vocab_size
        self.model_type = model_type
        self.max_sequence_length = max_sequence_length
        self.sp = None
        self.pad_id = 0  # SentencePiece reserves 0 for padding by default
        self.unk_id = 1  # Unknown token ID
        self.bos_id = 2  # Beginning of sequence ID
        self.eos_id = 3  # End of sequence ID

    def fit_on_texts(self, texts):
        """Train a SentencePiece tokenizer on the given texts"""
        try:
            # Create a temporary file to store the training data
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                for text in texts:
                    f.write(str(text).strip() + '\n')
                temp_path = f.name

            # Create model prefix
            model_prefix = os.path.join(tempfile.gettempdir(), f"med_sp_{self.vocab_size}")

            # Train SentencePiece model
            spm.SentencePieceTrainer.train(
                input=temp_path,
                model_prefix=model_prefix,
                vocab_size=self.vocab_size,
                model_type=self.model_type,  # "bpe" or "unigram"
                max_sentence_length=self.max_sequence_length,
                pad_id=self.pad_id,
                unk_id=self.unk_id,
                bos_id=self.bos_id,
                eos_id=self.eos_id,
                control_symbols=["[MED]", "[CHEM]", "[DIAG]"],  # Special tokens for medical domain
                user_defined_symbols=["<sep>", "<cls>", "<mask>"],
                character_coverage=0.9995,  # High coverage for medical terms
                normalization_rule_name="nmt_nfkc"  # Normalized text
            )

            # Load the trained model
            self.sp = spm.SentencePieceProcessor()
            self.sp.load(f"{model_prefix}.model")
            logger.info(f"SentencePiece model trained with vocabulary size: {self.sp.get_piece_size()}")

            # Cleanup temporary files
            os.unlink(temp_path)
            os.unlink(f"{model_prefix}.model")
            os.unlink(f"{model_prefix}.vocab")

        except Exception as e:
            logger.error(f"Error training SentencePiece model: {e}")
            raise

    def texts_to_sequences(self, texts):
        """Convert texts to integer sequences"""
        if not self.sp:
            raise ValueError("Tokenizer not trained. Call fit_on_texts first.")

        sequences = []
        for text in texts:
            # Encode text to integer sequence
            seq = self.sp.encode_as_ids(str(text))
            # Truncate or pad sequence
            if len(seq) > self.max_sequence_length:
                seq = seq[:self.max_sequence_length]
            else:
                seq = seq + [self.pad_id] * (self.max_sequence_length - len(seq))
            sequences.append(seq)
        return sequences

    def sequences_to_texts(self, sequences):
        """Convert integer sequences back to texts"""
        if not self.sp:
            raise ValueError("Tokenizer not trained. Call fit_on_texts first.")
            
        texts = []
        for seq in sequences:
            # Remove padding tokens
            seq = [id for id in seq if id != self.pad_id]
            # Decode sequence to text
            text = self.sp.decode_ids(seq)
            texts.append(text)
        return texts

    def save(self, path):
        """Save the tokenizer model"""
        if not self.sp:
            raise ValueError("No model to save. Train the tokenizer first.")
        self.sp.save(path)

    def load(self, path):
        """Load a saved tokenizer model"""
        self.sp = spm.SentencePieceProcessor()
        self.sp.load(path)
