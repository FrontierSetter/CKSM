. bert_3.7/bin/activate
export BERT_BASE_DIR=/home/l/workload/bert/bert/pre_model/uncased_L-12_H-768_A-12
export SQUAD_DIR=/home/l/workload/bert/bert/dataset/SQuAD_1_1

my_log="./" 
name="bert"
> ${my_log}"timestamp_bert.log"

for ((i=0;i<$1;i++))
do
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_bert.log"

    python run_squad.py   --vocab_file=$BERT_BASE_DIR/vocab.txt   --bert_config_file=$BERT_BASE_DIR/bert_config.json   --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt   --do_train=True   --train_file=$SQUAD_DIR/train-v1.1.json   --do_predict=True   --predict_file=$SQUAD_DIR/dev-v1.1.json   --train_batch_size=24   --learning_rate=3e-5   --num_train_epochs=2.0   --max_seq_length=384   --doc_stride=128   --output_dir=/tmp/squad_base/ &
    sleep 2
done

date +%s >> ${my_log}"timestamp_bert.log"
