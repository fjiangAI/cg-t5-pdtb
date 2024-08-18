CUDA_VISIBLE_DEVICES=0 nohup python3 test_joint.py \
--model_path=output_dir/question_first_endpoint/model-9 \
--des_file=result_detail_question_first_endpoint.txt \
--test_file=./data_dir/question_first/test.json \
--convert_type=question_first \
> test_question_first_endpoint.hup&