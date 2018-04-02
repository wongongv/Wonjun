what_i_received=[1,1,0,0,0,1,0,0,1,0,1,1,1,1,0,0,1,1,0,0,1,1,0,1,0,1,0,1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,0,0,1,0,1,1,0,1,1,0,1,1,1,0,0,0,1,0,1,1,1,1,1,1,1,0,1,1,0,0,1,0,1,0,0,0,1,0]
my_basis=[1,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,1,1,0,1,0,0,0,1,1,1,0,0,1,0,1,1,1,1,1,0,1,0,1,0,0,0,0,0,1,0,0,1]
alice_basis=[0,0,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,0,1,0,1,0,0,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,1,1,0,1,0,1,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,1,1,0,0,0,1,0,1,1,1,1,1,0,0,0,1,1,0,0,1]
what_i_received_under_matching_basis=[]
what_i_received_under_matching_basis_aft20=[]
alice_first_20_digit=[1,1,0,1,0,1,0,0,1,0,0,1,1,1,1,1,1,1,0,1]

-------------------------------------------------------------------------------------------------------------------------------
>>first of all, match my basis and alice's basis                                                                                                                              '
>>and compare first 20 key after discard datas under mismatched basis.
>> it gave me back 8 keys are wrong out of 20 which is 40% error rate.
>> there are many possibilities.
>> 1. somebody spied on it.
>> 2. because of noise. ex> optic fiber can alter the polarization of the light. (If they used light to send/receive the data)
-------------------------------------------------------------------------------------------------------------------------------
i=0
for a,b in zip(my_basis,alice_basis):
	if a==b:
		what_i_received_under_matching_basis+=[what_i_received[i]]
		if i>=20:
			what_i_received_under_matching_basis_aft20+=[what_i_received[i]]
		i+=1
	else:
		i+=1
-------------------------------------------------------------------------------------------------------------------------------
>>received a message
message=[0,0,1,1,0,0,0,1,1,1,1,0,1,0,0,1,0,1,1,1,0,0,0,0,0]
-------------------------------------------------------------------------------------------------------------------------------
>>Fileter the what_i_received data from 21 to 80 by discarding datas which received under mismatched basis
>>Add filtered bits to the message.
-------------------------------------------------------------------------------------------------------------------------------
result=[what_i_received_under_matching_basis_aft20[i]+message[i] for i in range(len(message))]
final_result=[]
for i in result:
	if i==2:
		final_result+=[0]
	else:
		final_result+=[i]
-------------------------------------------------------------------------------------------------------------------------------
>>Print final result
-------------------------------------------------------------------------------------------------------------------------------
print(final_result)
=> 10001 10101 00010 01001 10100
17 21 2 9 20
Decoding : Q U B I T
message : "QUBIT"
-------------------------------------------------------------------------------------------------------------------------------
We have received "QUBIT"