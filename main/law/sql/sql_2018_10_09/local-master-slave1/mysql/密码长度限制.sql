update user set authentication_string=password('HHly2017@') where `Host`='%'

select @@validate_password_policy; 
SHOW VARIABLES LIKE 'validate_password%'; 
set global validate_password_policy=0; 
FLUSH PRIVILEGES