CUDA_VISIBLE_DEVICES=0 nohup python3 train_joint.py \
--num_train_epochs=10 \
--train_batch_size=2 \
--test_batch_size=4 \
--device=0 \
--test_file_path=./data_dir/question_first/test.json \
--train_file_path=./data_dir/question_first/train.json \
--pretrained_model_path=./t5/ \
--data_dir=./data_dir/question_first/ \
--output_dir=./output_dir/question_first_endpoint/ \
--span_layer=endpoint  \
--generate_weight=1 \
--class_weight=1  > train_question_first_endpoint.hup&