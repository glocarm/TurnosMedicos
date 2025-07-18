PGDMP                      }            Turnos    16.3    16.3 0    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    75486    Turnos    DATABASE     {   CREATE DATABASE "Turnos" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';
    DROP DATABASE "Turnos";
                postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            ]           1247    83718    tipo_estado    TYPE     q   CREATE TYPE public.tipo_estado AS ENUM (
    'Pendiente',
    'Confirmado',
    'Cancelado',
    'Completado'
);
    DROP TYPE public.tipo_estado;
       public          postgres    false    4            W           1247    83700    tipo_usuario    TYPE     W   CREATE TYPE public.tipo_usuario AS ENUM (
    'Paciente',
    'Medico',
    'admin'
);
    DROP TYPE public.tipo_usuario;
       public          postgres    false    4            �            1259    75519    especialidades    TABLE     �   CREATE TABLE public.especialidades (
    id integer NOT NULL,
    nombrespec character varying(100) NOT NULL,
    descripcion text
);
 "   DROP TABLE public.especialidades;
       public         heap    postgres    false    4            �            1259    75518    especialidades_id_seq    SEQUENCE     �   CREATE SEQUENCE public.especialidades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.especialidades_id_seq;
       public          postgres    false    216    4            �           0    0    especialidades_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.especialidades_id_seq OWNED BY public.especialidades.id;
          public          postgres    false    215            �            1259    91871    horarios_medico    TABLE       CREATE TABLE public.horarios_medico (
    id integer NOT NULL,
    medico_id integer,
    dia_semana character varying(10),
    hora_inicio time without time zone,
    hora_fin time without time zone,
    duracion integer,
    activo boolean DEFAULT true
);
 #   DROP TABLE public.horarios_medico;
       public         heap    postgres    false    4            �            1259    91870    horarios_medico_id_seq    SEQUENCE     �   CREATE SEQUENCE public.horarios_medico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.horarios_medico_id_seq;
       public          postgres    false    222    4            �           0    0    horarios_medico_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.horarios_medico_id_seq OWNED BY public.horarios_medico.id;
          public          postgres    false    221            �            1259    75540    medicos    TABLE     '  CREATE TABLE public.medicos (
    id integer NOT NULL,
    nombremed character varying(50) NOT NULL,
    apellidomed character varying(50) NOT NULL,
    especialidad_id integer,
    telefono character varying(100),
    direccionmed character varying(200),
    cedulamed character varying(10)
);
    DROP TABLE public.medicos;
       public         heap    postgres    false    4            �            1259    75539    medicos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.medicos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.medicos_id_seq;
       public          postgres    false    218    4            �           0    0    medicos_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.medicos_id_seq OWNED BY public.medicos.id;
          public          postgres    false    217            �            1259    91884    turnos    TABLE     v   CREATE TABLE public.turnos (
    id integer NOT NULL,
    usuario_id integer,
    turno_id integer,
    fecha date
);
    DROP TABLE public.turnos;
       public         heap    postgres    false    4            �            1259    91883    turnos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.turnos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.turnos_id_seq;
       public          postgres    false    4    224            �           0    0    turnos_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.turnos_id_seq OWNED BY public.turnos.id;
          public          postgres    false    223            �            1259    83708    usuarios    TABLE       CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre character varying(50),
    apellido character varying(50),
    email character varying(100),
    contrasena character varying(255),
    tipo_usuario public.tipo_usuario DEFAULT 'Paciente'::public.tipo_usuario
);
    DROP TABLE public.usuarios;
       public         heap    postgres    false    855    4    855            �            1259    83707    usuarios_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.usuarios_id_seq;
       public          postgres    false    4    220            �           0    0    usuarios_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;
          public          postgres    false    219                       2604    75522    especialidades id    DEFAULT     v   ALTER TABLE ONLY public.especialidades ALTER COLUMN id SET DEFAULT nextval('public.especialidades_id_seq'::regclass);
 @   ALTER TABLE public.especialidades ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216                       2604    91874    horarios_medico id    DEFAULT     x   ALTER TABLE ONLY public.horarios_medico ALTER COLUMN id SET DEFAULT nextval('public.horarios_medico_id_seq'::regclass);
 A   ALTER TABLE public.horarios_medico ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    222    222                       2604    75543 
   medicos id    DEFAULT     h   ALTER TABLE ONLY public.medicos ALTER COLUMN id SET DEFAULT nextval('public.medicos_id_seq'::regclass);
 9   ALTER TABLE public.medicos ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    218    218                       2604    91887 	   turnos id    DEFAULT     f   ALTER TABLE ONLY public.turnos ALTER COLUMN id SET DEFAULT nextval('public.turnos_id_seq'::regclass);
 8   ALTER TABLE public.turnos ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223    224                       2604    83711    usuarios id    DEFAULT     j   ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);
 :   ALTER TABLE public.usuarios ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219    220            �          0    75519    especialidades 
   TABLE DATA           E   COPY public.especialidades (id, nombrespec, descripcion) FROM stdin;
    public          postgres    false    216   6       �          0    91871    horarios_medico 
   TABLE DATA           m   COPY public.horarios_medico (id, medico_id, dia_semana, hora_inicio, hora_fin, duracion, activo) FROM stdin;
    public          postgres    false    222   h6       �          0    75540    medicos 
   TABLE DATA           q   COPY public.medicos (id, nombremed, apellidomed, especialidad_id, telefono, direccionmed, cedulamed) FROM stdin;
    public          postgres    false    218   W7       �          0    91884    turnos 
   TABLE DATA           A   COPY public.turnos (id, usuario_id, turno_id, fecha) FROM stdin;
    public          postgres    false    224    8       �          0    83708    usuarios 
   TABLE DATA           Y   COPY public.usuarios (id, nombre, apellido, email, contrasena, tipo_usuario) FROM stdin;
    public          postgres    false    220   \8       �           0    0    especialidades_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.especialidades_id_seq', 5, true);
          public          postgres    false    215            �           0    0    horarios_medico_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.horarios_medico_id_seq', 205, true);
          public          postgres    false    221            �           0    0    medicos_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.medicos_id_seq', 8, true);
          public          postgres    false    217            �           0    0    turnos_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.turnos_id_seq', 9, true);
          public          postgres    false    223            �           0    0    usuarios_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.usuarios_id_seq', 6, true);
          public          postgres    false    219                       2606    75526 "   especialidades especialidades_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.especialidades
    ADD CONSTRAINT especialidades_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.especialidades DROP CONSTRAINT especialidades_pkey;
       public            postgres    false    216            &           2606    91877 $   horarios_medico horarios_medico_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.horarios_medico
    ADD CONSTRAINT horarios_medico_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.horarios_medico DROP CONSTRAINT horarios_medico_pkey;
       public            postgres    false    222                        2606    75545    medicos medicos_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.medicos
    ADD CONSTRAINT medicos_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.medicos DROP CONSTRAINT medicos_pkey;
       public            postgres    false    218            (           2606    91889    turnos turnos_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.turnos
    ADD CONSTRAINT turnos_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.turnos DROP CONSTRAINT turnos_pkey;
       public            postgres    false    224            "           2606    83716    usuarios usuarios_email_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);
 E   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_email_key;
       public            postgres    false    220            $           2606    83714    usuarios usuarios_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_pkey;
       public            postgres    false    220            *           2606    91878 .   horarios_medico horarios_medico_medico_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.horarios_medico
    ADD CONSTRAINT horarios_medico_medico_id_fkey FOREIGN KEY (medico_id) REFERENCES public.medicos(id);
 X   ALTER TABLE ONLY public.horarios_medico DROP CONSTRAINT horarios_medico_medico_id_fkey;
       public          postgres    false    4640    218    222            )           2606    75546 $   medicos medicos_especialidad_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.medicos
    ADD CONSTRAINT medicos_especialidad_id_fkey FOREIGN KEY (especialidad_id) REFERENCES public.especialidades(id);
 N   ALTER TABLE ONLY public.medicos DROP CONSTRAINT medicos_especialidad_id_fkey;
       public          postgres    false    216    218    4638            +           2606    91895    turnos turnos_turno_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.turnos
    ADD CONSTRAINT turnos_turno_id_fkey FOREIGN KEY (turno_id) REFERENCES public.horarios_medico(id);
 E   ALTER TABLE ONLY public.turnos DROP CONSTRAINT turnos_turno_id_fkey;
       public          postgres    false    222    224    4646            ,           2606    91890    turnos turnos_usuario_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.turnos
    ADD CONSTRAINT turnos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);
 G   ALTER TABLE ONLY public.turnos DROP CONSTRAINT turnos_usuario_id_fkey;
       public          postgres    false    4644    220    224            �   <   x�3��MM�L��KT��+I-�K���2�t��KM���O?�,b� T�XR���qqq rZ�      �   �   x�u�K
�0 ���0e2�|���E�U�����i�$��B�y�/ў�A?�Έ����J{�E	h!�"r��h��zt��د���m�
U��P,,Q<Si~3����3��>[�q�\ˤ~a���V�s����i��C�H�biI���?���o"�B�!xF�Bd�����.ų��^�H�� �t�^�#���7b�>��!l�?��I)�H��      �   �   x�]�K�0DדSp�8ZH�
$�\�
��Ϟ�qպ��Eƒ4��K+�L�s��H��M'���:D)Ej��טdx4왈B`ޱD��-��q֜����\��~���Q�cM5�t�1t}��`5&N�~�M���I�����}��G��Т-      �   L   x�M��� ���G����%��AQ�;Z����CKS�����I<)V�~�D{�~T��:�|�j��^��� �Y      �   �   x�}���0E�ӏ!Q�4���+7�Z��vL���W�ƅ˛s_)l붯8�y�o�D�b�y���C;%���"_��Cm���e�D/$�N�JA4����k��p�W�5��f3�K~�O�z�?�����|`g<�g�?[�g�0�n�]D�     