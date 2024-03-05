

# FreeCAD에서 복셀로 변환하기

FreeCAD에서 복셀 변환을 위해서는 OBJ 파일이 필요합니다. 이 파일을 복셀 프로그램으로 변환할 수 있습니다.

## 복셀 변환 프로그램 사용 실습

### voxel 명령어 사용

1. **복셀의 크기 지정**
   ```
   binvox -d 64 base.obj
   ```
   출력의 크기, 즉 복셀의 크기를 64 픽셀로 줄입니다.

2. **Z-버퍼 기반 조각 메서드만 사용**
   ```
   binvox -c model.obj
   ```

3. **교차점 전에 조각을 중지하는 확장 조각 사용**
   ```
   binvox -dc model.obj
   ```
   교차점 1 복셀 전에 조각을 중지합니다.

4. **Z-버퍼 기반 패리티 투표 메서드**
   ```
   binvox -v model.obj
   ```
   Z-버퍼 기반 조각 메서드만 사용합니다.

5. **다른 입력 모델 경계 상자 강제 사용**
   ```
   binvox -bb 0 0 0 125 125 125 model.obj
   ```
   경계 상자로 자릅니다.

6. **내부 복셀 삭제**
   ```
   binvox -ri model.obj
   ```

7. **정규화 진행**
   ```
   binvox -nf 0.5 model.obj
   ```
   정규화 계수를 사용합니다.

## binvox-rw-py 실습

### 코드 분석

1. **리드 헤더: 크기, 스케일, 변환 정보 제공**
   ```python
   def read_header(fp):
       line = fp.readline().strip()
       if not line.startswith(b'#binvox'):
           raise IOError('Not a binvox file')
       dims = list(map(int, fp.readline().strip().split(b' ')[1:]))
       translate = list(map(float, fp.readline().strip().split(b' ')[1:]))
       scale = list(map(float, fp.readline().strip().split(b' ')[1:]))[0]
       line = fp.readline()
       return dims, translate, scale
   
   with open('base_3.binvox', 'rb') as f:
       model = binvox_rw.read_header(f)
   
   print(model)
   ```
   출력값: `([64, 64, 64], [-7.87082, -8.18195, 1.0], 21.9527)`

2. **3D numpy 배열로 읽기**
   ```python
   import binvox_rw
   import numpy as np
   
   with open('base_3.binvox', 'rb') as f:
       model = binvox_rw.read_as_3d_array(f)
   
   print(model.dims, model.translate, model.scale, model.axis_order, model.data)
   ```
   출력값: `[64, 64, 64] [-7.87082, -8.18195, 1.0] 21.9527 xyz [[[False False False ... False False False] ...]]`

3. **좌표 배열로 읽기**
   ```python
   with open('base_3.binvox', 'rb') as f:
       model = binvox_rw.read_as_coord_array(f)
   
   print(model.data)
   ```
   출력값: `[[ 0  0  0 ... 63 63 63] [ 0  1  2 ... 23 24 25] [27 27 27 ... 36 36 36]]`

4. **3D numpy 배열을 좌표 배열로 변환**
   ```python
   with open('base_3.binvox', 'rb') as f:
       model = binvox_rw.read_as_3d_array(f)
       model = binvox_rw.dense_to_sparse(model.data)
   
   print(model)
   ```
   출력값: `[[ 0  0  0 ... 63 63 63] [ 0  0  0 ... 25 25 25] [27 28 29 ... 34

 35 36]]`

5. **좌표 배열을 3D numpy 배열로 변환**
   반대의 과정으로 진행됩니다.
